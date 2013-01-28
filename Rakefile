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

desc "Deploy site to production"
task :deploy do
  system "rm -rf _site"
  # TODO: Rewrite this script to cache the checked-out version of the
  #       site in a _deploy directory.
  #       
  #       That makes this script O(n) instead of O(n*m), where:
  #           n = size of site and
  #           m = number of prior deployments.
  system "git clone git@github.com:davidfstr/davidfstr.github.com.git _site"
  system "mv _site/.git /tmp/davidfstr.github.com-git"  # preserve .git
  system "rake dist"                                    # (will clobber _site)
  system "mv /tmp/davidfstr.github.com-git _site/.git"  # restore .git
  Dir.chdir("_site") do
    system "git add -A"
    system "git commit -m 'Deploy.'"
    system "git push -u origin master"
  end
end