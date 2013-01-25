task :default => [:preview]

desc "Compile / to /_sites and launch preview server"
task :preview do
  system "jekyll --auto --server"
end

desc "Compile /prism directory to /_sites"
task :prism do
  system "python _plugins/prism.py"
end

desc "Compile entire site to _sites"
task :build do
  system "jekyll --no-auto --no-server"
  system "python _plugins/prism.py"
end