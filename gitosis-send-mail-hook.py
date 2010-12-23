#!/usr/bin/python
__requires__ = 'gitosis==0.2'
import sys
import os
import logging
from logging.handlers import SysLogHandler
from gitosis import app
from ConfigParser import NoSectionError, NoOptionError


log = logging.getLogger('gitosis.send-mail-hook')

class Main(app.App):
	def __init__(self):
		self.setup_basic_logging()

	def _getMemberships(self,repository):
		to_inform=[]
		
		parser = self.create_parser()
		(options, args) = parser.parse_args()
		cfg = self.create_config(options)
		try:
			self.read_config(options, cfg)
		except CannotReadConfigError, e:
			log.error(str(e))
			sys.exit(1)
		
		for section in cfg.sections():
			GROUP_PREFIX = 'group '
			if not section.startswith(GROUP_PREFIX):
				continue
			group = section[len(GROUP_PREFIX):]

			all_reps=[]
			for rep_list in ("writable","readonly"):
				try:
					reps = cfg.get(section, rep_list)
				except (NoSectionError, NoOptionError):
					reps = []
				else:
					reps = reps.split()
				all_reps+=reps
		
			if repository in all_reps:
				try:
					members = cfg.get(section, 'members')
				except (NoSectionError, NoOptionError):
					members = []
				else:
					members = members.split()
				for member in members:
					if member not in to_inform:
						to_inform.append(member)
		log.debug("info to "+', '.join(to_inform))
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

