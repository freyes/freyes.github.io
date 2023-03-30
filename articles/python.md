Title: Python Snippets
Date: 2013-01-01
Category: Snippets
Tags: python, snippets

## Property

    :::python
    def Property(f):
        fget, fset, fdel = f()
        fdoc = f.__doc__
        return property(fget, fset, fdel, fdoc)

### Usage Example

    :::python
    class TtyExample (object):
    
        def __init__ (self):
            self._name = None
    
        @Property
        def name(f):
            "The name"
            def fget (self):
                return self._name
    
            def fset (self, value):
                assert isinstance (value, basestring)
                assert value != '', 'Name cannot be empty'
    
                self._name = value
    
            def fdel (self):
                print "Hey! don't delete me please :\ "
    
    if __name__ == "__main__":
        a = TtyExample()
        a.name='foobar'
        try:
            a.name = ''
        except:
            pass
    
        try:
            a.name = None
        except:
            pass
    
        del a.name

## Get my IP address

    :::python
    import socket
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("tty.cl",80))
    print s.getsockname()

### Example

<pre>
>>> import socket
>>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> s.connect(("tty.cl",80))
>>> print s.getsockname()
('10.0.0.10', 44883)
</pre>

## Get variables

    :::python
    import sys
    import traceback
    from StringIO import StringIO
    
    def print_exc(tb=None):
        """
        Print the usual traceback information, followed by a listing of all the
        local variables in each frame.
    
        :rtype StringIO.StringIO: all the traceback information
        """
        output = StringIO()
    
        if tb == None:
            print sys.exc_info()
            tb = sys.exc_info()[2]
    
        print tb
    
        while 1:
            if not tb.tb_next:
                break
            tb = tb.tb_next
        stack = []
        f = tb.tb_frame
        while f:
            stack.append(f)
            f = f.f_back
        stack.reverse()
        output.write("Locals by frame, innermost last\n")
        for frame in stack:
            output.write("Frame %s in %s at line %s\n" % (frame.f_code.co_name,
                                                          frame.f_code.co_filename,
                                                          frame.f_lineno))
            for key, value in frame.f_locals.items():
                output.write("\t%20s = " % key)
                #We have to be careful not to cause a new error in our error
                #printer! Calling str() on an unknown object could cause an
                #error we don't want.
                try:
                    output.write("%s\n" % value)
                except:
                    output.write("<ERROR WHILE PRINTING VALUE>\n")

    :::python
    import logging
    
    class SMSHandler(logging.Handler): # Inherit from logging.Handler
        def emit(self, record):
            print record
            import pdb
            pdb.set_trace()
    
    import logging.handlers
    
    # Create a logging object (after configuring logging)
    logging.basicConfig(filename="as",level=logging.WARNING)
    logger = logging.getLogger()
    
    # A little trickery because, at least for me, directly creating
    # an SMSHandler object didn't work
    logging.handlers.SMSHandler = SMSHandler
    
    # create the handler object
    testHandler = logging.handlers.SMSHandler()
    # Configure the handler to only send SMS for critical errors
    testHandler.setLevel(logging.CRITICAL)
    
    # and finally we add the handler to the logging object
    logger.addHandler(testHandler)
    
    # And finally a test
    logger.debug('Test 1')
    logger.info('Test 2')
    logger.warning('Test 3')
    logger.error('Test 4')
    logger.critical('Test 5')


## json encoder/decoder

    :::python
    import json
    import datetime
    
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    class JSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, datetime.datetime):
                return obj.strftime(DATETIME_FORMAT)
            else:
                return super(JSONEncoder, self).default(obj)
    
    
    class JSONDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, *args,
                                      object_hook=self.object_hook, **kwargs)
    
        def object_hook(self, obj):
            if isinstance(obj, dict):
                for key in obj:
                    if not isinstance(obj[key], basestring):
                        continue
                    try:
                        obj[key] = datetime.datetime.strptime(obj[key],
                                                              DATETIME_FORMAT)
                    except ValueError:
                        pass
    
            return obj
    
    if __name__ == "__main__":
        encoder = JSONEncoder()
        print encoder.encode({"date": datetime.datetime.now()})
    
        decoder = JSONDecoder()
        print decoder.decode(encoder.encode({"date": datetime.datetime.now()}))

## sendmail

    :::python
    import smtplib
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEBase import MIMEBase
    from email.MIMEText import MIMEText
    from email.Utils import COMMASPACE, formatdate
    from email import Encoders
    import os
    
    def sendMail(to, subject, text, files=[],server="localhost"):
        assert type(to)==list
        assert type(files)==list
        fro = "Expediteur <expediteur@mail.com>"
    
        msg = MIMEMultipart()
        msg['From'] = fro
        msg['To'] = COMMASPACE.join(to)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
    
        msg.attach( MIMEText(text) )
    
        for file in files:
            part = MIMEBase('application', "octet-stream")
            part.set_payload( open(file,"rb").read() )
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                           % os.path.basename(file))
            msg.attach(part)
    
        smtp = smtplib.SMTP(server)
        smtp.sendmail(fro, to, msg.as_string() )
        smtp.close()
    
    
    sendMail(
            ["destination@dest.kio"],
            "hello","cheers",
            ["photo.jpg","memo.sxw"]
        )

Original snippet available at http://snippets.dzone.com/posts/show/757
