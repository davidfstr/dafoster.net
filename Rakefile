task :default => [:preview]

desc "Compile / (except /prism) to /_sites and launch preview server"
task :preview do
  system "jekyll --auto --server"
end

desc "Compile /prism directory to /_sites"
task :prism do
  system "python _plugins/prism.py"
end

desc "Compile entire site to _sites in preparation for deployment"
task :dist do
  # TODO: Signify deployment readiness by means other than the "safe" flag.
  system "jekyll --no-auto --no-server --safe"
  system "python _plugins/prism.py"
  system "touch _site/.nojekyll"
end