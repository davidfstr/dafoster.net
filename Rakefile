task :default => [:preview]

desc "Compile main site (except prism) to _site and launch preview server"
task :preview do
  puts "Starting preview server at: http://localhost:4000/"
  system "jekyll serve --config _config.yml,_config-develop.yml --watch --trace"
end

desc "Launch preview server and visit it in a web browser."
task :go do
  Thread.new { sleep 5; system 'open "http://localhost:4000/"' }
  system "rake preview"
end

desc "Compile prism subsite to _site"
task :prism do
  system "python _plugins/prism.py"
end

desc "Compile entire site to _site in production mode"
task :dist do
  abort unless system "python _plugins/checkdates.py"
  
  # Compile site
  # NOTE: Production mode is signified by site.develop=false
  system "jekyll build --config _config.yml"
  system "python _plugins/prism.py"
  
  # Apply post-compile modifications
  system "touch _site/.nojekyll"
  system "rm _site/project.sublime-workspace"
end

# Deployment performance should be O(n + m), where:
#   n = size of site and
#   m = number of changed files since last deployment
desc "Deploy site to production"
task :deploy do
  # Detect whether a preview server is running.
  require "socket"
  begin
    socket = TCPSocket.open("localhost", 4000)
    socket.close
    
    preview_server_running = true
  rescue # Errno::ECONNREFUSED
    preview_server_running = false
  end
  
  if preview_server_running
    jekyll_pid_str = `pgrep -f "^ruby /usr/share/rvm/gems/ruby-.*/bin/jekyll serve"`.strip    
    if jekyll_pid_str != ""
      # Did find preview server
      jekyll_pid = Integer(jekyll_pid_str)
    else
      # Preview server is running but was not found
      puts "*** It looks like a preview server is running,"
      puts "*** and cannot be automatically paused."
      puts "*** Please stop it before attempting to deploy."
      abort
    end
  end
  
  if preview_server_running
    # Pause the preview server
    # (If such a server is running in "auto" mode, it will mess around with
    #  the _site directory while this script is operating on it.)
    system "kill -s STOP #{jekyll_pid}"
  end
  begin
    # Download latest version of production, if not already done
    if not File.directory? '_production/.git'
      puts "Cloning davidfstr.github.com..."
      system "rm -rf _production"
      system "git clone git@github.com:davidfstr/davidfstr.github.com.git _production"
    else
      puts "Pulling davidfstr.github.com..."
      Dir.chdir("_production") do
        system "git checkout master"
        system "git pull --ff-only"
      end
    end
    
    # Link _site -> _production
    system "rm -rf _site"
    system "ln -s _production _site"
    begin
      # Regenerate entire site in _site (and _production), preserving .git
      system "mkdir -p _production_build"
      begin
        system "mv _production/.git _production_build/git"  # preserve .git
        begin
          abort unless system "rake dist"  # (will clobber contents of _site)
        ensure
          system "mv _production_build/git _production/.git"  # restore .git
        end
      ensure
        system "rm -rf _production_build"
      end
      
      # Add .nojekyll to avoid unnecessary Jekyll processing of the compiled site
      # after deployment
      system "touch _production/.nojekyll"
      
      # Push new version of production site
      Dir.chdir("_production") do
        system "git add -A"
        system "git commit -m 'Deploy.'"
        system "git push -u origin master"
      end
    ensure
      # Unlink _site from _production
      system "rm _site"
    end
  ensure
    if preview_server_running
      # Resume the preview server
      system "kill -s CONT #{jekyll_pid}"
    end
  end
end