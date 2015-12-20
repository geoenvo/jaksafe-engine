# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import pandas as pd

import config

class Summary(object):

    """
    Ringkasan informasi hasil perhitungan DaLA

    :param time_0: waktu awal kejadian banjir
    :param time_1: waktu akhir kejadian banjir (waktu dimulainya perhitungan DaLA)
    """

    def __init__(self, time_0, time_1, tipe='auto'):

        """
        Menginisiasi kelas Summary
        """

        self.time_0 = time_0
        self.time_1 = time_1

        self.path = config.Path(time_0, time_1, tipe=tipe)
        self.subs = config.Subsektor()

    def normalize(self, jenis, asuransi=False):

        """
        Menormalisasi Dataframe pandas

        :param df_input: Dataframe pandas yang akan dinormalisasi
        :param aset: jenis aset
        """

        # input
        dala_file = self.path.output_dir + 'dala_' + \
            self.time_0 + '_' + self.time_1 + '.csv'

        if asuransi:
            dala_file = self.path.output_dir + 'dala_asuransi_' + \
                self.time_0 + '_' + self.time_1 + '.csv'

        # dataframe
        df_dala = pd.read_csv(dala_file)

        # remove jenis lainnya
        daftar_jenis = ['KERUGIAN', 'KERUSAKAN']
        daftar_jenis.remove(jenis)

        # grouping dataframe
        grouping = ['SUBSEKTOR', 'ASET', 'KOTA']
        df_dala.drop(daftar_jenis, inplace=True, axis=1)
        df_dala = df_dala.groupby(grouping, as_index=False).sum()
        df_dala = df_dala.set_index(grouping)

        # change the innermost pandas index into columns
        df_dala = df_dala.unstack()
        df_dala = df_dala[jenis]

        # ordering column
        new_order = ([
            'JAKARTA UTARA',
            'JAKARTA SELATAN',
            'JAKARTA PUSAT',
            'JAKARTA BARAT',
            'JAKARTA TIMUR'
        ])
        df_dala = df_dala.reindex_axis(new_order, axis=1)

        # remove KOTA on column index
        df_dala = df_dala.reset_index()
        df_dala.columns.name = None

        # anticipate if one of column not exist
        anticipate = 0
        for n in new_order:
            if not n in df_dala.columns:
                print n
                anticipate += 1
                df_dala[n] = 0

        if anticipate > 0:
            new_order = ([
                'SUBSEKTOR',
                'ASET',
                'JAKARTA UTARA',
                'JAKARTA SELATAN',
                'JAKARTA PUSAT',
                'JAKARTA BARAT',
                'JAKARTA TIMUR'
            ])
            df_dala = df_dala.reindex_axis(new_order, axis=1)

        # new name
        new_name = ([
            'SUBSEKTOR',
            'ASET',
            'JAKUT',
            'JAKSEL',
            'JAKPUS',
            'JAKBAR',
            'JAKTIM'
        ])
        df_dala.columns = new_name

        # change not a number (nan) to zero
        df_dala.fillna(0, inplace=True)

        # total
        df_dala['TOTAL'] = df_dala.sum(axis=1)

        # insert sector in the beginning
        daftar_sektor = []
        for i in df_dala.ASET.values:
            daftar_sektor.append(self.subs.get_sektor(aset=i))
        df_dala.insert(0, 'SEKTOR', daftar_sektor)

        # set index
        df_dala.set_index(['SEKTOR', 'SUBSEKTOR', 'ASET'], inplace=True)

        return df_dala

    def summarize(self):

        """
        Meringkas hasil perhitungan DaLA ke Panel pandas

        :return: properti df_summary
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        return pn_summary

    def total(self):

        """
        Mendapatkan nilai total dari kerugian atau kerusakan

        :return: nilai kerugian dan kerusakan total dalam bentuk dictionary
        """

        total = {
            'KERUSAKAN' : self.summarize()['KERUSAKAN'].sum().TOTAL,
            'KERUGIAN' : self.summarize()['KERUGIAN'].sum().TOTAL,
        }

        return total

    def get_data_bar_page_1(self):

        """
        Mendapatkan data untuk grafik batang pada halaman 1
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        array_rusak = df_rusak.groupby(level=0).sum().TOTAL.values
        array_rugi = df_rugi.groupby(level=0).sum().TOTAL.values

        data = {}
        data['array_rusak'] = array_rusak
        data['array_rugi'] = array_rugi
        data['x_labels'] = df_rugi.index.levels[0]

        return data

    def get_data_table_page_1(self):

        """
        Mendapatkan data untuk tabel pada halaman 1
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        source = {
            'SEKTOR' : [],
            'KERUSAKAN' : [],
            'KERUGIAN' : [],
            'TOTAL' : [],
            'FLAG' : []
        }

        # merge subsektor and sektor
        index = []
        sector = {}

        index.append([df_rusak.index.levels[0], 0])
        index.append([df_rusak.index.levels[1], 1])

        for i in index:
            for n in i[0]:
                sector[n] = i[1]

        # calculate data
        for s in sector:
            source['SEKTOR'].append(s)
            nilai_rusak = df_rusak.sum(axis=0, level=sector[s]).TOTAL[s]
            nilai_rugi = df_rugi.sum(axis=0, level=sector[s]).TOTAL[s]
            source['KERUSAKAN'].append(nilai_rusak)
            source['KERUGIAN'].append(nilai_rugi)
            source['TOTAL'].append(nilai_rusak + nilai_rugi)
            source['FLAG'].append(sector[s])

        df_source = pd.DataFrame(source)
        df_source = df_source.set_index('SEKTOR')
        df_source['NUMBERING'] = xrange(len(df_source))
        df_source['NUMBERING'] = df_source['NUMBERING'] + 1

        # todo list
        # sorting berdasarkan urutan yang seperti di fsd
        labels = ([
            'PRODUKTIF',
            'PERTANIAN',
            'PERDAGANGAN',
            'INDUSTRI',
            'PARIWISATA',
            'SOSIAL DAN PERUMAHAN',
            'PERUMAHAN',
            'KESEHATAN',
            'PENDIDIKAN',
            'INFRASTRUKTUR',
            'TRANSPORTASI',
            'TELEKOMUNIKASI',
            'ENERGI',
            'AIR BERSIH DAN SANITASI',
            'LINTAS SEKTOR',
            'PEMERINTAHAN',
            'FINANSIAL',
            'AGAMA',
            'LINGKUNGAN'
        ])
        df_source = df_source.reindex_axis(labels, axis='index')
        # antisipasi ketika tidak semua list labels ditampilkan
        df_source = df_source[df_source.KERUGIAN.notnull()]
        df_source = df_source.reset_index()

        df_data_sum = df_source[df_source.FLAG==0]

        data = {
            'df_source' : df_source,
            'df_data_sum' : df_data_sum
        }

        return data

    def get_data_bar_page_2(self):

        """
        Mendapatkan data untuk grafik batang pada halaman 2
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        array_rusak = df_rusak.groupby(level=1).sum().TOTAL.values
        array_rugi = df_rugi.groupby(level=1).sum().TOTAL.values

        data = {}
        data['array_rusak'] = array_rusak
        data['array_rugi'] = array_rugi
        data['x_labels'] = df_rugi.index.levels[1]

        return data

    def get_data_pie_page_3(self):

        """
        Mendapatkan data untuk grafik lingkaran pada halaman 3
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        array_rusak = df_rusak.groupby(level=1).sum().TOTAL.values
        array_rugi = df_rugi.groupby(level=1).sum().TOTAL.values

        data = {}
        data['array_rusak'] = array_rusak
        data['array_rugi'] = array_rugi
        data['pie_labels'] = df_rugi.index.levels[1]

        return data

    def get_data_table_page_4_and_5(self):

        """
        Mendapatkan data untuk grafik batang pada halaman 2
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6
        df_rusak['FIRST'] = False
        df_rusak['FLAG'] = False
        df_rusak['LAST'] = False
        df_rugi['FIRST'] = False
        df_rugi['FLAG'] = False
        df_rugi['LAST'] = False

        # get list of first aset in subsector
        first_index = []
        for i in df_rusak.index.levels[1]:
            first_index.append(df_rusak.xs(i, level=1).ix[0].name[1])

        # change value of first to true in each first index
        df_rusak = df_rusak.reset_index()
        df_rugi = df_rugi.reset_index()
        for f in first_index:
            df_rusak.loc[df_rusak.ASET == f, 'FIRST'] = True
            df_rugi.loc[df_rugi.ASET == f, 'FIRST'] = True

        # get list of last aset in subsector
        df_rusak = df_rusak.set_index(['SEKTOR', 'SUBSEKTOR', 'ASET'])
        df_rugi = df_rugi.set_index(['SEKTOR', 'SUBSEKTOR', 'ASET'])
        last_index = []
        for i in df_rusak.index.levels[1]:
            last_index.append(df_rusak.xs(i, level=1).ix[-1].name[1])

        # change value of flag to true in each last index
        df_rusak = df_rusak.reset_index()
        df_rugi = df_rugi.reset_index()
        for l in last_index:
            df_rusak.loc[df_rusak.ASET == l, 'FLAG'] = True
            df_rugi.loc[df_rugi.ASET == l, 'FLAG'] = True

        # mekanisme sorting sehingga urutan sesuai dengan fsd
        df_rusak = df_rusak.set_index(['SEKTOR', 'SUBSEKTOR', 'ASET'])
        df_rugi = df_rugi.set_index(['SEKTOR', 'SUBSEKTOR', 'ASET'])
        sorted_labels_sektor = ([
            'PRODUKTIF',
            'SOSIAL DAN PERUMAHAN',
            'INFRASTRUKTUR',
            'LINTAS SEKTOR'
        ])
        sorted_labels_subsektor = ([
            'PERTANIAN',
            'PERDAGANGAN',
            'INDUSTRI',
            'PARIWISATA',
            'PERUMAHAN',
            'KESEHATAN',
            'PENDIDIKAN',
            'TRANSPORTASI',
            'TELEKOMUNIKASI',
            'ENERGI',
            'AIR BERSIH DAN SANITASI',
            'PEMERINTAHAN',
            'LINGKUNGAN',
            'FINANSIAL',
            'AGAMA'
        ])
        df_rusak = df_rusak.reindex_axis(sorted_labels_sektor, axis='index', level=0)
        df_rugi = df_rugi.reindex_axis(sorted_labels_sektor, axis='index', level=0)
        df_rusak = df_rusak.reindex_axis(sorted_labels_subsektor, axis='index', level=1)
        df_rugi = df_rugi.reindex_axis(sorted_labels_subsektor, axis='index', level=1)

        # antisipasi ketika tidak semua list labels ditampilkan
        df_rusak = df_rusak[df_rusak.JAKUT.notnull()]
        df_rugi = df_rugi[df_rugi.JAKUT.notnull()]

        # change last row of column last to true
        df_rusak.ix[-1, 'LAST'] = True
        df_rugi.ix[-1, 'LAST'] = True

        # rename nama yang terlalu panjang
        df_rusak.rename(index={'AIR BERSIH DAN SANITASI': 'AIR BERSIH'}, inplace=True)
        df_rusak.rename(index={'TELEKOMUNIKASI': 'TELEKOM'}, inplace=True)
        df_rusak.rename(index={'TELEKOMUNIKASI': 'TELEKOM'}, inplace=True)
        df_rusak.rename(index={'OBYEK WISATA DAN LAYANAN TURIS': 'OBYEK WISATA'}, inplace=True)
        df_rusak.rename(index={'BONGKAR MUAT PELABUHAN': 'PELABUHAN'}, inplace=True)
        df_rusak.rename(index={'FASILITAS KEPOLISIAN': 'FAS. KEPOLISIAN'}, inplace=True)
        df_rusak.rename(index={'FASILITAS MILITER': 'FAS. MILITER'}, inplace=True)
        df_rusak.rename(index={'FASILITAS PEMERINTAHAN': 'FAS. PEMERINTAHAN'}, inplace=True)
        df_rugi.rename(index={'AIR BERSIH DAN SANITASI': 'AIR BERSIH'}, inplace=True)
        df_rugi.rename(index={'TELEKOMUNIKASI': 'TELEKOM'}, inplace=True)
        df_rugi.rename(index={'TELEKOMUNIKASI': 'TELEKOM'}, inplace=True)
        df_rugi.rename(index={'OBYEK WISATA DAN LAYANAN TURIS': 'OBYEK WISATA'}, inplace=True)
        df_rugi.rename(index={'BONGKAR MUAT PELABUHAN': 'PELABUHAN'}, inplace=True)
        df_rugi.rename(index={'FASILITAS KEPOLISIAN': 'FAS. KEPOLISIAN'}, inplace=True)
        df_rugi.rename(index={'FASILITAS MILITER': 'FAS. MILITER'}, inplace=True)
        df_rugi.rename(index={'FASILITAS PEMERINTAHAN': 'FAS. PEMERINTAHAN'}, inplace=True)

        # change all but first row of subsektor to empty string
        df_rusak = df_rusak.reset_index()
        df_rusak.drop('SEKTOR', inplace=True, axis=1)
        df_rusak.loc[df_rusak.FIRST == False, 'SUBSEKTOR'] = ''
        df_rugi = df_rugi.reset_index()
        df_rugi.drop('SEKTOR', inplace=True, axis=1)
        df_rugi.loc[df_rugi.FIRST == False, 'SUBSEKTOR'] = ''

        data = {}
        data['KERUSAKAN'] = df_rusak
        data['KERUGIAN'] = df_rugi

        return data

    def get_data_bar_page_6(self):

        """
        Mendapatkan data untuk membuat grafik batang pada halaman 6
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6
        df_rusak.drop('TOTAL', inplace=True, axis=1)
        df_rugi.drop('TOTAL', inplace=True, axis=1)

        array_rusak = df_rusak.sum()
        array_rugi = df_rugi.sum()

        data = {}
        data['array_rusak'] = array_rusak.values
        data['array_rugi'] = array_rugi.values
        data['x_labels'] = array_rusak.index

        return data

    def get_data_bar_per(self, subsektor):

        """
        Mendapatkan data untuk membuat grafik batang perhitungan dala per
        subsektor
        """

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN'),
            'KERUGIAN' : self.normalize('KERUGIAN')
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        df_rusak.drop('TOTAL', inplace=True, axis=1)
        df_rugi.drop('TOTAL', inplace=True, axis=1)

        df_rusak = df_rusak.reset_index(0, drop=True)
        df_rugi = df_rugi.reset_index(0, drop=True)

        # select pandas dataframe that index in level=0 is subsektor
        df_rusak = df_rusak.xs(subsektor, level=0)
        df_rugi = df_rugi.xs(subsektor, level=0)

        # somehow important
        bottom_rusak = df_rusak.cumsum()
        bottom_rugi = df_rugi.cumsum()

        data = {}
        data['df_rusak'] = df_rusak
        data['df_rugi'] = df_rugi
        data['bottom_rusak'] = bottom_rusak
        data['bottom_rugi'] = bottom_rugi

        return data

    def get_data_asuransi(self):

        """
        Mendapatkan data untuk pelaporan dala asuransi
        """

        # read config penetrasi asuransi
        pene_file = self.path.assumption_dir + 'asumsi_penetrasiasuransi.csv'
        df_pene = pd.read_csv(pene_file)

        masking = ((df_pene.ASET != 'ASURANSI') | (df_pene['INSURANCE TYPE'] != 'PROPERTY'))
        df_pene = df_pene[masking]

        pn_summary = pd.Panel({
            'KERUSAKAN' : self.normalize('KERUSAKAN', asuransi=True),
            'KERUGIAN' : self.normalize('KERUGIAN', asuransi=True)
        })

        df_rusak = pn_summary['KERUSAKAN'] / 1e6
        df_rugi = pn_summary['KERUGIAN'] / 1e6

        asuransi_rusak = df_rusak.sum()
        asuransi_rugi = df_rugi.sum()
        total_rusak = df_rusak.sum()
        total_rugi = df_rugi.sum()
        total_detil = df_rugi.sum()

        # asuransi_detil
        df_rusak = df_rusak.reset_index()
        df_rugi = df_rugi.reset_index()
        df_rugi = df_rugi.merge(df_pene)
        column_drop = ([
            'PENETRASI ASURANSI',
            'KOTA',
            'KECAMATAN',
            'KELURAHAN'
        ])
        df_rugi.drop(column_drop, axis=1, inplace=True)
        df_rugi = df_rugi.groupby('INSURANCE TYPE').sum()
        df_rugi['FLAG'] = False
        df_rugi['FIRST'] = False
        df_rugi['SUBSEKTOR'] = 'FINANSIAL'
        df_rugi['ASET'] = 'ASURANSI'
        df_rugi.ix[-1, 'FLAG'] = True
        df_rugi.ix[0, 'FIRST'] = True
        df_rugi.loc[df_rugi.FIRST == False, 'SUBSEKTOR'] = ''
        df_rugi.loc[df_rugi.FIRST == False, 'ASET'] = ''
        df_rugi.rename(index={'GENERAL ACCIDENT':'ACCIDENT'}, inplace=True)
        df_rugi = df_rugi.reset_index()

        new_name = ([
            'JENIS_ASURANSI',
            'JAKUT',
            'JAKSEL',
            'JAKPUS',
            'JAKBAR',
            'JAKTIM',
            'TOTAL',
            'FLAG',
            'FIRST',
            'SUBSEKTOR',
            'ASET',
        ])
        df_rugi.columns = new_name

        new_order = ([
            'SUBSEKTOR',
            'ASET',
            'JENIS_ASURANSI',
            'JAKUT',
            'JAKSEL',
            'JAKPUS',
            'JAKBAR',
            'JAKTIM',
            'TOTAL',
            'FLAG',
            'FIRST'
        ])
        df_rugi = df_rugi.reindex_axis(new_order, axis=1)
        df_table = df_rugi.drop(['SUBSEKTOR', 'ASET', 'FLAG', 'FIRST', 'TOTAL'], axis=1)
        df_table = df_table.set_index('JENIS_ASURANSI')
        bottom_rugi = df_table.cumsum()

        print df_rugi
        print df_table.index
        print bottom_rugi

        data = {}
        data['asuransi_rusak'] = asuransi_rusak
        data['asuransi_rugi'] = asuransi_rugi
        data['asuransi_detil'] = df_rugi
        data['total_rusak'] = total_rusak
        data['total_rugi'] = total_rugi
        data['total_detil'] = total_detil
        data['df_table'] = df_table
        data['bottom_rugi'] = bottom_rugi

        return data
