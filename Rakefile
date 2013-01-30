task :default => [:preview]

desc "Compile main site (except prism) to _site and launch preview server"
task :preview do
  system "jekyll --auto --server"
end

desc "Compile prism subsite to _site"
task :prism do
  system "python _plugins/prism.py"
end

desc "Compile entire site to _site in production mode"
task :dist do
  # TODO: Signify deployment readiness by means other than the "safe" flag.
  system "jekyll --no-auto --no-server --safe"
  system "python _plugins/prism.py"
  system "touch _site/.nojekyll"
end

# Deployment performance should be O(n + m), where:
#   n = size of site and
#   m = number of changed files since last deployment
desc "Deploy site to production"
task :deploy do
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
  
  # Push new version of production site
  Dir.chdir("_production") do
    system "git add -A"
    system "git commit -m 'Deploy.'"
    system "git push -u origin master"
  end
  
  # Unlink _site from _production
  system "rm _site"
end