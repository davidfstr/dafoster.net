task :default => [:preview]

desc "Compile main site (except prism) to _site and launch preview server"
task :preview do
  puts "Starting preview server at: http://localhost:4000/"
  system "jekyll --server --auto"
end

desc "Compile prism subsite to _site"
task :prism do
  system "python _plugins/prism.py"
end

desc "Compile entire site to _site in production mode"
task :dist do
  # NOTE: Production mode is signified by server=false
  system "jekyll --no-server --no-auto"
  system "python _plugins/prism.py"
  system "touch _site/.nojekyll"
end

# Deployment performance should be O(n + m), where:
#   n = size of site and
#   m = number of changed files since last deployment
desc "Deploy site to production"
task :deploy do
  # Refuse to deploy if it looks like a preview server is running.
  # (If such a server is running in "auto" mode, it will mess around with
  #  the _site directory while this script is operating on it.)
  require "socket"
  begin
    socket = TCPSocket.open("localhost", 4000)
    socket.close
    
    puts "*** It looks like a preview server is running."
    puts "*** Please stop it before attempting to deploy."
    ok_to_deploy = false
  rescue # Errno::ECONNREFUSED
    ok_to_deploy = true
  end
  
  if ok_to_deploy
    # Download latest version of production, if not already done
    if not File.directory? '_production/.git'
      system "rm -rf _production"
      system "git clone git@github.com:davidfstr/davidfstr.github.com.git _production"
    else
      Dir.chdir("_production") do
        system "git checkout master"
        system "git pull"
      end
    end
    
    # Link _site -> _production
    system "rm -rf _site"
    system "ln -s _production _site"
    
    # Regenerate entire site in _site (and _production), preserving .git
    system "mv _production/.git /tmp/davidfstr.github.com-git"  # preserve .git
    system "rake dist"  # (will clobber contents of _site)
    system "mv /tmp/davidfstr.github.com-git _production/.git"  # restore .git
    
    # Add .nojekyll to avoid unnecessary Jekyll processing of the compiled site
    # after deployment
    system "touch _production/.nojekyll"
    
    # Push new version of production site
    Dir.chdir("_production") do
      system "git add -A"
      system "git commit -m 'Deploy.'"
      system "git push -u origin master"
    end
    
    # Unlink _site from _production
    system "rm _site"
  end
end