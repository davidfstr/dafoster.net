---
layout: post
title: CompressedTextField for Django & MySQL is released!
tags: [Software]

---

I'm proud to release [django-mysql-compressed-fields]: a new library that
provides a *compressed* version of Django's TextField for use with a MySQL
[^postgres] database! This is the first library from [TechSmart] to be
open-sourced. 🎉

In particular you can replace a [TextField] or [CharField] like:

[TextField]: https://docs.djangoproject.com/en/3.2/ref/models/fields/#textfield
[CharField]: https://docs.djangoproject.com/en/3.2/ref/models/fields/#charfield

```python
from django.db import models

class ProjectTextFile(models.Model):
    content = models.TextField(blank=True)
```

with:

```python
from django.db import models
from mysql_compressed_fields import CompressedTextField

class ProjectTextFile(models.Model):
    content = CompressedTextField(blank=True)
```

such that the text value of the field is actually compressed in the database.

String-based lookups are supported:

```python
html_files = ProjectTextFile.objects.filter(content__contains='<html')
html_files = ProjectTextFile.objects.filter(content__startswith='<!DOCTYPE')
html_files = ProjectTextFile.objects.filter(content__endswith='</html>')
empty_html_files = ProjectTextFile.objects.filter(content__in=['', '<html></html>'])
```

Advanced manipulations with MySQL's [COMPRESS()], [UNCOMPRESS()], and 
[UNCOMPRESSED_LENGTH()] functions are also supported:

```python
from django.db.models import F
from mysql_compressed_fields import UncompressedLength

files = ProjectTextFile.objects.only('id').annotate(
    content_length=UncompressedLength(F('content'))
)
```

For more information, including how to [migrate to use CompressedTextField],
please see the [documentation].


[django-mysql-compressed-fields]: https://github.com/techsmartkids/django-mysql-compressed-fields#readme
[TextField]: https://docs.djangoproject.com/en/3.2/ref/models/fields/#textfield
[TechSmart]: https://www.techsmart.codes/
[migrate to use CompressedTextField]: https://github.com/techsmartkids/django-mysql-compressed-fields#migration-steps
[documentation]: https://github.com/techsmartkids/django-mysql-compressed-fields#readme

[COMPRESS()]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_compress
[UNCOMPRESS()]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompress
[UNCOMPRESSED_LENGTH()]: https://dev.mysql.com/doc/refman/5.7/en/encryption-functions.html#function_uncompressed-length

[^postgres]: My understanding is that the Postgres database - another database type that works well with Django - transparently compresses all text fields automatically, so a library like this one wouldn't be useful for users of that database.