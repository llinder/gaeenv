import logging
import os


def mkdir(path):
    """
    Create directory
    """
    if not os.path.exists(path):
        logger.debug(' * Creating: %s ... ', path)
        os.makedirs(path)
        logger.debug('done.')
    else:
        logger.debug(' * Directory %s already exists', path)


def writefile(dest, content, overwrite=True, append=False, encode="utf-8"):
    """
    Create file and write content in it
    """
    if not os.path.exists(dest):
        logger.debug(' * Writing %s ... ', dest)
        f = open(dest, 'wb')
        if encode:
            f.write(content.encode(encode))
        else:
            f.write(content)
        f.close()
        logger.debug('done.')
        return
    else:
        f = open(dest, 'rb')
        c = f.read()
        f.close()
        if c != content:
            if not overwrite:
                logger.info(' * File %s exists with different content; '
                            ' not overwriting', dest)
                return
            if append:
                logger.info(' * Appending nodeenv settings to %s', dest)
                f = open(dest, 'a')
                f.write(DISABLE_POMPT.encode('utf-8'))
                f.write(content.encode('utf-8'))
                f.write(ENABLE_PROMPT.encode('utf-8'))
                f.close()
                return
            logger.info(' * Overwriting %s with new content', dest)
            f = open(dest, 'wb')
            if encode:
                f.write(content.encode(encode))
            else:
                f.write(content)
            f.close()
        else:
            logger.debug(' * Content %s already in place', dest)


def create_logger():
    """
    Create logger for diagnostic
    """
    # create logger
    logger = logging.getLogger("gaeenv")
    logger.setLevel(logging.ERROR)

    # monkey patch
    def emit(self, record):
        msg = self.format(record)
        fs = "%s" if getattr(record, "continued", False) else "%s\n"
        self.stream.write(fs % msg)
        self.flush()
    logging.StreamHandler.emit = emit

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter(fmt="%(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    return logger

logger = create_logger()
    