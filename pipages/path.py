import os
import shutil

class File:
	def __init__(self, path):
		self.path = path

	def abspath(self):
		return File(os.path.abspath(self.path))

	def normpath(self):
		return File(os.path.normpath(self.path))

	def join(self, *args):
		return File(os.path.join(self.path, *args))

	def exists(self):
		return os.path.exists(self.path)

	def rmtree(self):
		if self.exists():
			shutil.rmtree(self.path)

	def parent(self):
		return File(os.path.dirname(self.path))

	def chdir(self):
		return chdir(self.path)

	def makedirs(self):
		if not self.exists():
			os.makedirs(self.path)

	def __str__(self):
		return self.path

class chdir:
	def __init__(self, path):
		self.path = path
		self.old_cwd = None

	def __enter__(self):
		self.old_cwd = os.getcwd()
		os.chdir(self.path)

	def __exit__(self, *a, **kw):
		os.chdir(self.old_cwd)
