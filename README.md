# Website 3.0

This is the personal website of [David Foster].

## Why should I care?

You may be interested in reading the source code if you want an **example of 
how a complex [Jekyll] site is structured**. Notable features include:

* **[breadcrumbs]** on all pages
* **clean URLs** that lack file extensions (or query parameters)
* **advanced Markdown** with footnotes and multi-level bulleted lists
* **deployment automation** to [GitHub Pages] via [git]
* a **[tag index]** for blog posts
    * ...including anchor-based header highlighting

Have specific questions about how these were implemented? [Contact me].

[David Foster]: https://github.com/davidfstr
[Jekyll]: https://github.com/mojombo/jekyll
[breadcrumbs]: http://en.wikipedia.org/wiki/Breadcrumb_(navigation)
[git]: http://git-scm.com
[GitHub Pages]: http://pages.github.com
[tag index]: http://dafoster.net/articles/topics/#Software
[Contact me]: http://dafoster.net/contact/

## Installation

* Clone this repository:
    * `git clone https://github.com/davidfstr/dafoster.net`
    * `cd dafoster.net`
* Install [Docker]
* Build Docker image:
    * `docker build -t dafoster.net .`
* Create and start Docker container, if not already created:
    * `docker run --name dafoster.net -it -v `pwd`:/home -v $HOME/.ssh:/root/.ssh:ro -p 4000:4000 -d dafoster.net:latest`

[Docker]: https://www.docker.com/

## Usage

##### Run local webserver with the website at: <http://127.0.0.1:4000/>

```
docker start dafoster.net
# (Wait 5-10 seconds for the server to start)
docker exec -it dafoster.net bash --login -c "rake prism"   # Optional
open http://127.0.0.1:4000/
```

##### Compile to `_site` directory in production mode

```
docker exec -it dafoster.net bash --login -c "rake dist"
```

##### Deploy to GitHub Pages

```
$ docker exec -it dafoster.net bash --login
$$ eval "$(ssh-agent -s)"  # start SSH agent
$$ ssh-add  # login to GitHub
$$ rake deploy
$$ exit
```

##### Open shell inside Docker container

```
docker exec -it dafoster.net bash --login
```

## License

Copyright &copy; 2013-2021 by David Foster. All rights reserved.
