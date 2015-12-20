__AUTHOR__ = 'Abdul Somat Budiaji'

import logging

import MySQLdb as ms

logger = logging.getLogger('jakservice.post_processing.db')

class DBase(object):

    """
    Antar muka untuk database mysql
    """

    def __init__(self, params):

        # pass
        self.host = params['host']
        self.user = params['user']
        self.passwd  = params['passwd']
        self.db = params['db']
        self.port = params['port']

        # connect to database
        try:
            self.con = ms.connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                db = self.db,
                port = self.port
            )
        except:
            exit(1)

    def close(self):

        """
        Menutup koneksi ke database
        """

        if self.con:
            self.con.close()

    def write(self, table, data):

        """
        Menulis data ke dalam tabel

        :param table: tabel di dalam databse untuk menyimpan data
        :param data: data yang akan disimpan
        """

        logger.info('Dbase.write')

        cursor = self.con.cursor()

        q_data = (table, data['t0'], data['t1'], data['damage'], data['loss'])

        q_write = '''
        INSERT INTO %s (t0, t1, damage, loss) VALUES ('%s', '%s','%s', '%s')
        ''' %q_data

        try:
            row = cursor.execute(q_write)
            self.con.commit()
        except Exception, e:
            logger.error(e)
            self.con.rollback()

        return row

    def update(self, table, data):

        """
        Mengupdate data ke dalam tabel

        :param table: tabel di dalam databse untuk menyimpan data
        :param data: data yang akan disimpan
        """

        logger.info('Dbase.update')

        cursor = self.con.cursor()

        q_data = (table, data['damage'], data['loss'], data['id'])

        q_write = '''
        UPDATE %s SET damage='%s', loss='%s' WHERE id='%s'
        ''' %q_data

        try:
            row = cursor.execute(q_write)
            self.con.commit()
        except Exception, e:
            logger.error(e)
            self.con.rollback()

        return row
