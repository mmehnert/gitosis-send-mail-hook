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

	def _getDevelopers(self,repository):
		emails_to_inform=[]
		
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

			repositories_in_current_group=[]
			for repository_access_list in ("writable","readonly"):
				try:
					tmp_repositories = cfg.get(section, repository_access_list)
				except (NoSectionError, NoOptionError):
					tmp_repositories = []
				else:
					tmp_repositories = tmp_repositories.split()
				repositories_in_current_group+=tmp_repositories
		
			if repository in repositories_in_current_group:
				try:
					group_members = cfg.get(section, 'members')
				except (NoSectionError, NoOptionError):
					group_members = []
				else:
					group_members = group_members.split()
				for member in group_members:
					if member not in emails_to_inform:
						emails_to_inform.append(member)
		log.debug("info to "+', '.join(emails_to_inform))
		return emails_to_inform

	@classmethod
	def getDevelopers(class_,repository):
		app = class_()
		return app._getDevelopers(repository)
		
if __name__ == '__main__':
	repository, ext = os.path.splitext(os.getcwd())
	if ext != '.git':
		log.error(os.getcwd()+"is probably not a gitosis repository.")
		sys.exit(1)
	repository=os.path.basename(repository)
	print ', '.join(Main.getDevelopers(repository))

