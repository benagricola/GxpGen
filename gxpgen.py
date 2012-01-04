#!/usr/bin/env python
from __future__ import with_statement

import os, sys, logging, binascii, struct, urllib, errno
import common.config as config

b_crlf = "\x0D\x0A\x0D\x0A"

def chunks(l, n):
	for i in xrange(0, len(l), n):
		yield l[i:i+n]

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError, exc: # Python >2.5
        if exc.errno == errno.EEXIST:
            pass
        else: raise
		

	
class GXPGen(object):

	file_config = os.path.join(sys.path[0],'gxpgen.conf')
	templates = {}
	
	def replace_values(self,lines,values):
		o = []
		for key,value in lines.items():

			o.append("%s=%s" % (key,urllib.quote(value % values)))
			
		return '&'.join(o)
		
	def main(self):
		self.parse_config()
		self.start_logging()
		self.load_templates()

		# Iterate over all phones in config, generate template, save files
	
		self.log.info('Found %d phones in config...' % (len(self.cfg.phones)))
		for name in self.cfg.phones:
			details = self.cfg.phones[name]
			
			# Build up value dict for assigning values to template
			values = dict(self.cfg.equipment)
			values['phone_name'] = name
			
			values.update(details)
			
			tpl_str = self.populate_template(self.templates[details.template],values)
	
			tpl_str += "&gnkey=%s" % (details.mac.lower()[2:6])
			
			b_mac = binascii.unhexlify(details.mac.replace(':', ''))
			self.log.info("Populated template for phone '%s'" % (name))
			
			if (len(tpl_str) % 2) != 0:
				tpl_str += "\x00" 
			if (len(tpl_str) % 4) != 0:
				tpl_str += "\x00\x00" 
		
		
			tpl_length = 8 + (len(tpl_str)/2);
		
		
			b_length = struct.pack('>H',tpl_length)
			self.log.info("Calculating length...")
			
			b_string = b_length + b_mac + b_crlf + tpl_str
			
			self.log.info("Checksumming...")
			csv = 0
			for c in chunks(b_string,2):
				csv += struct.unpack('>H',c)[0]

			checksum = 0x10000 - csv
			checksum &= 0xFFFF
			
			b_checksum = struct.pack(">H", checksum)

			fp = os.path.join(sys.path[0],self.cfg.output_dir)
			
			# Create path if not exists
			mkdir_p(fp)
			
			fp = os.path.join(fp,'cfg%s' % (details.mac.lower()))
			
			self.log.info("Writing config for '%s' to '%s'" % (name,fp))
		
			with open(fp,'wb') as of:
				of.write("\x00\x00")
				of.write(b_length)
				of.write(b_checksum)
				of.write(b_mac)
				of.write("\x0D\x0A\x0D\x0A")
				of.write(tpl_str)
			
	
	def load_templates(self):
		for template in self.cfg.templates:
			tp = file(os.path.join(sys.path[0],'templates',template)).readlines()
			self.templates[template] = tp
	
	def populate_template(self,tp,values):
		op = []
		for line in tp:
			line = line.strip()
	
			if line.startswith('#'):
				continue
			
			try:
				var,value = line.split(' =',1)
				op.append("%s=%s" % (var.strip(),urllib.quote(value.strip() % values,'')))
				
			except ValueError:
				if line != '':
					print "Syntax error on line: '%s'" % (line)
				continue
		
		return '&'.join(op)
		
	def parse_config(self):
		self.cfg = config.Config(file(self.file_config))
	
	def start_logging(self):
        # Set up file logging
		format_string = self.cfg.logging.file_format
		log_format = logging.Formatter(format_string)
		logging.basicConfig(level=self.cfg.logging.file_debug_level, format=format_string, filename=self.cfg.logging.location,filemode='a')

		console_log = logging.StreamHandler()
		console_log.setLevel(self.cfg.logging.console_debug_level)
		clog_format = logging.Formatter(self.cfg.logging.console_format)
		console_log.setFormatter(clog_format)
		logging.getLogger('').addHandler(console_log)
			
		self.log = logging.getLogger('MAIN')
		self.log.info('Starting Up')

        
	
if __name__ == "__main__":   
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    
    p = GXPGen()
    p.main()