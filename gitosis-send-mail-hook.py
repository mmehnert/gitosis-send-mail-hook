#!/usr/bin/python
__requires__ = 'gitosis==0.2'
import sys
import os
from gitosis import app


class Main(app.App):
	def _getMemberships(self,repository):
		parser = self.create_parser()
		(options, args) = parser.parse_args()
		cfg = self.create_config(options)
		try:
			self.read_config(options, cfg)
		except CannotReadConfigError, e:
			log.error(str(e))
			sys.exit(1)
		to_inform=[]
		
		for section in cfg.sections():
			GROUP_PREFIX = 'group '
			if not section.startswith(GROUP_PREFIX):
				continue
			group = section[len(GROUP_PREFIX):]
	
			try:
				writable = cfg.get(section, 'writable')
			except (NoSectionError, NoOptionError):
				writable = []
			else:
				writable = writable.split()
	
			if repository in writable:
				try:
					members = cfg.get(section, 'members')
				except (NoSectionError, NoOptionError):
					members = []
				else:
					members = members.split()
				for member in members:
					if member not in to_inform:
						to_inform.append(member)
		return to_inform

	@classmethod
	def getMemberships(class_,repository):
		app = class_()
		return app._getMemberships(repository)
		
if __name__ == '__main__':
	repository, ext = os.path.splitext(os.getcwd())
	if ext != '.git':
		print os.getcwd()+"is probably not a gitosis repository."
		sys.exit(1)
	repository=os.path.basename(repository)
	print ', '.join(Main.getMemberships(repository))

