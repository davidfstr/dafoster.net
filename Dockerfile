# 
# Runs the Jekyll static site generator.
# 

FROM ubuntu:14.04

# Setup directories
WORKDIR /home

# Ensure apt packages are up-to-date
RUN apt-get update && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# Install en_US.UTF-8 locale
RUN apt-get install language-pack-en -y
ENV LC_ALL="en_US.UTF-8"

# Install Python
RUN apt-get install python -y  # Python 2.7

# Install Git (latest)
RUN apt-get install git -y && \
    git config --global user.email "david@dafoster.net" && \
    git config --global user.name "David Foster"

# Install RVM (latest)
# https://github.com/rvm/ubuntu_rvm
RUN apt-get install software-properties-common -y
SHELL ["/bin/bash", "--login", "-c"]
RUN apt-add-repository -y ppa:rael-gc/rvm && \
        apt-get update && \
        apt-get install rvm -y

# Install Ruby
RUN rvm install "ruby-2.4" && \
    rvm use ruby-2.4@website --create

# Install Bundler
RUN gem install bundler:1.17.3  # last bundler that allows ruby < 2.3.0

# Install dependencies
COPY ./Gemfile /home/
COPY ./Gemfile.lock /home/
RUN bundle install

EXPOSE 4000
CMD ["/bin/bash", "--login", "-c", "rake preview"]
