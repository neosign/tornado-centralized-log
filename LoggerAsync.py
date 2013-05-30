import tornado.ioloop
import tornado.web
import tornado.options
import logging
import logging.handlers
from pprint import pprint
import json
import time
from tornado import gen
from tornado.web import asynchronous

LOG_FILENAME = '/home/handbreak/public_html/pylog/sso'

logger = logging.getLogger('myapp')
#hdlr = logging.FileHandler(LOG_FILENAME)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#hdlr.setFormatter(formatter)
#logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
tornado.options.parse_command_line()


#handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,when='H',interval=1, backupCount=24)
handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,when='S',interval=10, backupCount=24)
handler.suffix = "%Y-%m-%d %H:%M:%S"+'.log' # or anything else that strftime will allow
handler.setFormatter(formatter)
logger.addHandler(handler)

def delist_arguments(args):
    """
    Takes a dictionary, 'args' and de-lists any single-item lists then
    returns the resulting dictionary.

    In other words, {'foo': ['bar']} would become {'foo': 'bar'}
    """
    for arg, value in args.items():
        if len(value) == 1:
            args[arg] = value[0]
    return args


class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.engine
    def get(self):
	response = yield gen.Task(self.logWrite)
	self.write('1')
	self.finish()
	#self.logWrite('test')

    @asynchronous
    @gen.engine
    def post(self):
	#self.logWrite("test")
	response = yield gen.Task(self.logWrite)
        self.write('1')
        self.finish()

    def logWrite(self,callback):
	#args = None
        # Sanitize argument lists:
        #if self.request.arguments:
        args = delist_arguments(self.request.arguments)
	jsonData = json.dumps(args)
	#pprint(args)
	logger.info(jsonData)
	#self.write("1")
	return callback('1')
    def testcall(msg,callback):
	time.sleep(2)
	return callback('done')
	
    def delist_arguments(args):
    	for arg, value in args.items():
            if len(value) == 1:
                args[arg] = value[0]
    	return args

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":

    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
