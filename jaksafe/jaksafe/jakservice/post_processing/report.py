# coding = utf-8
__AUTHOR__ = 'Abdul Somat Budiaji'

import datetime
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.font_manager import FontProperties
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib._png import read_png
from matplotlib.cbook import get_sample_data

import pandas as pd
import numpy as np

import config

################################################################################

# font properties
font_prop = {
    # format yang digunakan untuk tulisan dalam sel tabel
    'cell_normal' : FontProperties(size=9),
    # format yang digunakan untuk tulisan khusus dalam sel tabel
    'cell_bold' : FontProperties(size=9, weight='bold'),
    # format yang digunakan untuk label sumbu x suatu grafik
    'x_tick' : FontProperties(size=10),
    # format yang digunakan pada subjudul dan sebagainya
    'normal_font' : FontProperties(weight='bold', size=12),
    # format yang digunakan pada judul
    'title_font' : FontProperties(weight='bold', size=16)
}

################################################################################

class CraftCell():

    """
    Kelas untuk meramu sel individu dari objek Axes matplotlib
    (matplotlib.axes.Axes)

    :param init_row: koordinat awal baris (row)
    :param init_column: koordinat awal kolom (column)
    """

    def __init__(self, init_column, init_row, height_cell=0.02, width_cell=0.2):

        """
        Inisiasi kelas CraftCell
        """

        self.irow = init_row
        self.icolumn = init_column
        self.hcell = height_cell
        self.wcell = width_cell

    def insert_cell(self, fig, nrow, ncol):

        """
        Insert sel

        :param fig: figure matplotlib
        :param nrow: baris ke-n
        :param ncol: kolom ke-n

        :return: object axes matplotlib
        """

        row_coord = self.irow - nrow * self.hcell
        col_coord = self.icolumn + ncol * self.wcell

        ax = fig.add_axes(
            [col_coord, row_coord, self.wcell, self.hcell],
            frame_on=False,
            xticks=[],
            yticks=[])

        return ax

    def insert_text(self,
        fig,
        nrow,
        ncol,
        text_content,
        jenis='teks',
        underline=False,
        bold=False,
        box=False,
        color='#ffffff',
        width=1):

        ax = self.insert_cell(fig, nrow, ncol)
        arg_input = (0.0, 0.35, text_content)
        kwarg_input = {
            'fontproperties' : font_prop['cell_normal']
        }

        if (jenis=='teks') and (bold == True):
            kwarg_input = {
                'fontproperties' : font_prop['cell_bold']
            }
        elif (jenis=='angka') and (bold == False):
            # somehow can't execute this
            text_content = '{:,.0f}'.format(int(text_content))
            arg_input = (0.98, 0.35, text_content)
            kwarg_input = {
                'fontproperties' : font_prop['cell_normal'],
                'ha' : 'right'
            }
        elif (jenis=='angka') and (bold == True):
            text_content = '{:,.0f}'.format(int(text_content))
            arg_input = (0.98, 0.35, text_content)
            kwarg_input = {
                'fontproperties' : font_prop['cell_bold'],
                'ha' : 'right'
            }

        ax.text(*arg_input, **kwarg_input)

        if box:
            ax.axhspan(0, 1, color=color)

        if underline:
            ax.axhline(color='k', lw=width)

    def insert_text_blues(self, fig, nrow, ncol, text_content, underline=False):

        ax = self.insert_cell(fig, nrow, ncol)
        ax.text(
            0.5,
            0.35,
            text_content,
            fontproperties=font_prop['cell_bold'],
            ha='center')
        ax.axhspan(0, 1, color='#72ADED')
        if underline:
            ax.axhline(color='k')

    def insert_text_oranges(self, fig, nrow, ncol, text_content, underline=False):

        ax = self.insert_cell(fig, nrow, ncol)
        ax.text(
            0.5,
            0.35,
            text_content,
            fontproperties=font_prop['cell_bold'],
            ha='center')
        ax.axhspan(0, 1, color='#EDB272')
        if underline:
            ax.axhline(color='k')

    def insert_number_oranges(self, fig, nrow, ncol, text_content, underline=False):

        number_content = '{:,.0f}'.format(int(text_content))
        ax = self.insert_cell(fig, nrow, ncol)
        ax.text(
            0.98,
            0.35,
            number_content,
            fontproperties=font_prop['cell_bold'],
            ha='right')
        ax.axhspan(0, 1, color='#EDB272')
        if underline:
            ax.axhline(color='k')

################################################################################

class PdfFigure():

    """
    Kanvas untuk membuat pdf dari figure

    :paaram pdf_file: nama dari file pdf
    """

    def __init__(self, pdf_file):

        """
        Inisiasi kelas PdfFigure
        """

        self.fig = plt.figure(figsize=(8.27,11.68), dpi=100)
        self.pdf_pages = PdfPages(pdf_file)

        self.colors = (
            'aliceblue',
            'aquamarine',
            'azure',
            'bisque',
            'blanchedalmond',
            'chartreuse',
            'cornflowerblue',
            'darkkhaki',
            'darkorange',
            'dodgerblue',
            'fuchsia',
            'honeydew',
            'lemonchiffon',
            'mistyrose',
            'sienna'
        )

    def clear_figure(self):

        """
        Membersihkan figure
        """

        self.fig.clf()

    def finish_pdf(self):

        """
        Menutup proses penulisan figure ke file pdf
        """

        self.pdf_pages.close()

    def write_pdf(self):

        """
        Menulis figure ke file pdf
        """

        self.pdf_pages.savefig(self.fig)

    def page_title(self, image_dir):

        """
        Membuat judul laporan
        """

        s_title = '''Penilaian Kerusakan dan Kerugian
        Banjir Jakarta
        '''

        # logo jaksafe
        image = image_dir + 'jaksafe1.png'
        arr = plt.imread(image)

        ax_image = self.fig.add_axes(
            [0.1, 0.87, 0.1, 0.08],
            frame_on=False,
            xticks=[],
            yticks=[])
        ax_jaksafe = self.fig.add_axes(
            [0.2, 0.87, 0.13, 0.08],
            frame_on=False,
            xticks=[],
            yticks=[])
        ax_title = self.fig.add_axes(
            [0.33,0.87,0.57,0.08],
            frame_on=False,
            xticks=[],
            yticks=[])
        ax_title.text(
            0.5,0, s_title,
            fontproperties=font_prop['title_font'],
            ha='center')
        ax_jaksafe.text(
            0, 0.1, 'jakSAFE',
            fontproperties=font_prop['title_font'], color='#72ADED')

        # menambahkan logo jaksafe
        ax_image.imshow(arr)

    def page_date(self, time_0, time_1):

        """
        Membuat bagian tanggal di laporan halaman 1

        :param date_0: tanggal awal perhitungan DaLA
        :param date_1: tanggal akhir perhitungan DaLA
        """

        string_tanggal = 'Tanggal kejadian: %s - %s' %(time_0, time_1)

        ax_date = self.fig.add_axes(
            [0.1,0.84,0.8,0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_date.text(0, 0.25, string_tanggal, fontproperties=font_prop['normal_font'])

    def page_subtitle(self, subjudul, page_1=True):

        """
        Membuat subjudul laporan

        :param subjudul: Subjudul halaman yang bersangkutan
        :param page_1: (default True) Nilai kebenaran apakah halaman satu atau
            bukan
        """

        if page_1:
            s_subtitle = subjudul
            ax_subtitle = self.fig.add_axes([0.1,
                0.81,0.8,0.02],
                frame_on=False, xticks=[], yticks=[])
            ax_subtitle.text(0, 0.25, s_subtitle, fontproperties=font_prop['normal_font'])
        else:
            s_subtitle = subjudul
            ax_subtitle = self.fig.add_axes(
                [0.1,0.84,0.8,0.02],
                frame_on=False, xticks=[], yticks=[])
            ax_subtitle.text(0, 0.25, s_subtitle, fontproperties=font_prop['normal_font'])

    def page_bar(self, data):

        """
        Membuat grafik batang setengah halaman pada halaman 1

        :param data: data untuk membuat grafik batang setengah halaman pada
            halaman 1
        """

        # data
        array_rusak = data['array_rusak']
        array_rugi = data['array_rugi']

        # bar plot configuration
        x_labels = data['x_labels']

        bar_width = 0.2
        index = np.arange(len(x_labels)) + 0.1
        x_loc_tick = np.arange(len(x_labels)) + 0.2

        ax_bar = self.fig.add_axes([0.18,0.1,0.6,0.25], frame_on=True)

        ax_bar.bar(
            index, array_rusak,
            bar_width, color=self.colors[0],
            label='KERUSAKAN')
        ax_bar.bar(
            index, array_rugi,
            bar_width, color=self.colors[1],
            bottom=array_rusak,
            label='KERUGIAN')

        y_format = ticker.FuncFormatter('{:,.0f}'.format)
        ax_bar.yaxis.set_major_formatter(y_format)
        plt.xticks(x_loc_tick, x_labels, fontproperties=font_prop['x_tick'])

        ax_bar.legend(fontsize='xx-small', loc=(1.03,0))

    def page_half_table(self, data):

        """
        Membuat tabel setengah halaman pada halaman 1

        :param data: data untuk membuat tabel setengah halaman pada halaman 1
        """

        # create table
        cell = CraftCell(0.1, 0.78)

        # first row
        cell.insert_text_blues(self.fig, 0, 0, 'SEKTOR')
        cell.insert_text_blues(self.fig, 0, 1, 'KERUSAKAN')
        cell.insert_text_blues(self.fig, 0, 2, 'KERUGIAN')
        cell.insert_text_blues(self.fig, 0, 3, 'TOTAL')

        # data
        df_source = data['df_source']
        df_data_sum = data['df_data_sum']

        # content row
        # data
        for index, row in df_source.iterrows():
            # subsektor
            if row.FLAG == 1:
                cell.insert_text(self.fig, index+1, 0, row.SEKTOR)
                cell.insert_text(self.fig, index+1, 1, row.KERUSAKAN, jenis='angka')
                cell.insert_text(self.fig, index+1, 2, row.KERUGIAN, jenis='angka')
                cell.insert_text(self.fig, index+1, 3, row.TOTAL, jenis='angka')

            # sektor, font bold
            elif row.FLAG == 0:
                cell.insert_text(self.fig, index+1, 0,row.SEKTOR, bold=True)
                cell.insert_text(self.fig, index+1, 1, row.KERUSAKAN, jenis='angka', bold=True)
                cell.insert_text(self.fig, index+1, 2, row.KERUGIAN, jenis='angka', bold=True)
                cell.insert_text(self.fig, index+1, 3, row.TOTAL, jenis='angka', bold=True)

        # last row
        last_row = max(df_source.NUMBERING.values) + 1
        sum_data = df_data_sum.sum()
        cell.insert_text_oranges(self.fig, last_row, 0, 'TOTAL')
        cell.insert_number_oranges(self.fig, last_row, 1, sum_data.KERUSAKAN)
        cell.insert_number_oranges(self.fig, last_row, 2, sum_data.KERUGIAN)
        cell.insert_number_oranges(self.fig, last_row, 3, sum_data.TOTAL)

        cell = None

    def page_full_table(self, data, jenis):

        """
        Membuat table satu halaman penuh di halaman 4 dan 5

        :param data: data yang digunakan untuk membuat table pada halaman 4 dan 5
        :param jenis: KERUSAKAN atau KERUGIAN
        """

        # data
        df_data = data[jenis]

        # create table
        cell = CraftCell(0.02, 0.815, height_cell=0.015, width_cell=0.12)

        # row 0
        cell.insert_text_oranges(self.fig, 0, 0, '')
        cell.insert_text_oranges(self.fig, 0, 1, '')
        cell.insert_text_oranges(self.fig, 0, 2, '')
        cell.insert_text_oranges(self.fig, 0, 3, '')
        cell.insert_text_oranges(self.fig, 0, 4, 'KERUGIAN')
        cell.insert_text_oranges(self.fig, 0, 5, '')
        cell.insert_text_oranges(self.fig, 0, 6, '')
        cell.insert_text_oranges(self.fig, 0, 7, 'TOTAL')

        # row 1
        cell.insert_text_oranges(self.fig, 1, 0, 'SUBSEKTOR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 1, 'ASET', underline=True)
        cell.insert_text_oranges(self.fig, 1, 2, 'JAKUT', underline=True)
        cell.insert_text_oranges(self.fig, 1, 3, 'JAKSEL', underline=True)
        cell.insert_text_oranges(self.fig, 1, 4, 'JAKPUS', underline=True)
        cell.insert_text_oranges(self.fig, 1, 5, 'JAKBAR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 6, 'JAKTIM', underline=True)
        cell.insert_text_oranges(self.fig, 1, 7, '', underline=True)

        # for row 2 until last row -1
        for index, row in df_data.iterrows():
            if row.LAST == True:
                cell.insert_text(self.fig, index + 2, 0, row.SUBSEKTOR, underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 1, row.ASET, underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 2, row.JAKUT, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 3, row.JAKSEL, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 4, row.JAKPUS, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 5, row.JAKBAR, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 6, row.JAKTIM, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 7, row.TOTAL, jenis='angka', underline=True, width=2.5)
            elif row.FLAG == True:
                cell.insert_text(self.fig, index + 2, 0, row.SUBSEKTOR, underline=True)
                cell.insert_text(self.fig, index + 2, 1, row.ASET, underline=True)
                cell.insert_text(self.fig, index + 2, 2, row.JAKUT, jenis='angka', underline=True)
                cell.insert_text(self.fig, index + 2, 3, row.JAKSEL, jenis='angka', underline=True)
                cell.insert_text(self.fig, index + 2, 4, row.JAKPUS, jenis='angka', underline=True)
                cell.insert_text(self.fig, index + 2, 5, row.JAKBAR, jenis='angka', underline=True)
                cell.insert_text(self.fig, index + 2, 6, row.JAKTIM, jenis='angka', underline=True)
                cell.insert_text(self.fig, index + 2, 7, row.TOTAL, jenis='angka', underline=True)
            else:
                cell.insert_text(self.fig, index + 2, 0, row.SUBSEKTOR)
                cell.insert_text(self.fig, index + 2, 1, row.ASET)
                cell.insert_text(self.fig, index + 2, 2, row.JAKUT, jenis='angka')
                cell.insert_text(self.fig, index + 2, 3, row.JAKSEL, jenis='angka')
                cell.insert_text(self.fig, index + 2, 4, row.JAKPUS, jenis='angka')
                cell.insert_text(self.fig, index + 2, 5, row.JAKBAR, jenis='angka')
                cell.insert_text(self.fig, index + 2, 6, row.JAKTIM, jenis='angka')
                cell.insert_text(self.fig, index + 2, 7, row.TOTAL, jenis='angka')

        # last_row
        last_row = len(df_data) + 3
        sum_last = df_data.sum()
        cell.insert_text(self.fig, last_row, 0, 'Total', bold=True)
        cell.insert_text(self.fig, last_row, 1, '')
        cell.insert_text(self.fig, last_row, 2, sum_last.JAKUT, jenis='angka', bold=True)
        cell.insert_text(self.fig, last_row, 3, sum_last.JAKSEL, jenis='angka', bold=True)
        cell.insert_text(self.fig, last_row, 4, sum_last.JAKPUS, jenis='angka', bold=True)
        cell.insert_text(self.fig, last_row, 5, sum_last.JAKBAR, jenis='angka', bold=True)
        cell.insert_text(self.fig, last_row, 6, sum_last.JAKTIM, jenis='angka', bold=True)
        cell.insert_text(self.fig, last_row, 7, sum_last.TOTAL, jenis='angka', bold=True)

        cell = None


    def page_half_bar(self, data, subtitle):

        """
        Membuat grafik batang pada halaman 2

        :param data: data yang digunakan untuk membuat grafik batang pada
            halaman 2
        :param subtitle: subjudul yang digunakan pada halaman tersebut
        """

        # data
        array_rusak = data['array_rusak']
        array_rugi = data['array_rugi']

        # bar plot configuration
        x_labels = data['x_labels']

        # normalize to length 15 (default) ?
        len_index = len(x_labels)

        bar_width = 0.67
        index = np.arange(len_index) + 0.1
        x_loc_tick = np.arange(len(x_labels)) + 0.3

        ax_title = self.fig.add_axes(
            [0.1, 0.84, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_bar = self.fig.add_axes([0.18, 0.475, 0.5, 0.34], frame_on=True)

        ax_title.text(0, 0.25, subtitle, fontproperties=font_prop['normal_font'])

        ax_bar.bar(
            index, array_rusak,
            bar_width, color=self.colors[0],
            label='KERUSAKAN')
        ax_bar.bar(
            index, array_rugi,
            bar_width, color=self.colors[1],
            bottom=array_rusak,
            label='KERUGIAN')

        y_format = ticker.FuncFormatter('{:,.0f}'.format)
        ax_bar.yaxis.set_major_formatter(y_format)
        plt.xticks(x_loc_tick, x_labels, fontproperties=font_prop['x_tick'], rotation='vertical')

        ax_bar.legend(fontsize='xx-small', loc=(1.03, 0))

    def page_half_pie(self, data, subtitle):

        """
        Membuat grafik lingkaran pada halaman 3

        :param data: data yang digunakan untuk membuat grafik pada halaman
            tersebut
        :param subtitle: subjudul pada halaman tersebut
        """

        # data
        array_rusak = data['array_rusak']
        array_rugi = data['array_rugi']
        pie_labels = data['pie_labels']

        # kerusakan
        ax_title_top = self.fig.add_axes(
            [0.1, 0.84, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_pie_top = self.fig.add_axes([0.18,0.475,0.5,0.34], frame_on=True)

        ax_title_top.text(0, 0.25, subtitle[0], fontproperties=font_prop['normal_font'])

        pie_tuple = ax_pie_top.pie(
            array_rusak, autopct='%1.0f%%', labels=pie_labels,
            pctdistance=1.1, colors=self.colors)
        ax_pie_top.legend(fontsize='xx-small', loc=(1.03,0))

        # set visible is artist's method
        for i in pie_tuple[1]:
            i.set_visible(False)

        for i in pie_tuple[2]:
            i.set_fontsize(8)

        # kerugian
        ax_title_bottom = self.fig.add_axes(
            [0.1, 0.43, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_pie_bottom = self.fig.add_axes([0.18,0.065,0.5,0.34], frame_on=True)

        ax_title_bottom.text(0, 0.25, subtitle[1], fontproperties=font_prop['normal_font'])

        pie_tuple = ax_pie_bottom.pie(
            array_rugi, autopct='%1.0f%%', labels=pie_labels,
            pctdistance=1.1, colors=self.colors)
        ax_pie_bottom.legend(fontsize='xx-small', loc=(1.03,0))

        for i in pie_tuple[1]:
            i.set_visible(False)

        for i in pie_tuple[2]:
            i.set_fontsize(8)

    def page_summary_region(self, data, subtitle):

        """
        Membuat table batang pada halaman 6 untuk meringkas perhitungan
        dala pada semua wilayah

        :param data: data untuk membuat grafik batang pada halaman tersebut
        :param subtitle: subjudul pada halaman tersebut
        """

        # data
        array_rusak = data['array_rusak']
        array_rugi = data['array_rugi']

        x_labels = data['x_labels']

        # bar plot configuration
        len_index = len(x_labels)
        bar_width = 0.2
        index = np.arange(len_index) + 0.1

        ax_title = self.fig.add_axes(
            [0.1, 0.84, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_bar = self.fig.add_axes([0.18,0.475,0.5,0.34], frame_on=True)

        ax_title.text(0, 0.25, subtitle, fontproperties=font_prop['normal_font'])

        ax_bar.bar(
            index, array_rusak,
            bar_width, color=self.colors[0],
            label='KERUSAKAN')
        ax_bar.bar(
            index, array_rugi,
            bar_width, color=self.colors[1],
            bottom=array_rusak,
            label='KERUGIAN')

        y_format = ticker.FuncFormatter('{:,.0f}'.format)
        ax_bar.yaxis.set_major_formatter(y_format)
        plt.xticks(index, x_labels, fontproperties=font_prop['x_tick'])

        ax_bar.legend(fontsize='xx-small', loc=(1.03,0))

    def page_region_bar(self, data, subtitle):

        """
        Membuat grafik batang untuk merangkum perhitungan dala per subsektor

        :param data: data untuk membuat grafik batang pada halaman tersebut
        :param subtitle: subjudul untuk masing-masing grafik batang
        """

        # data
        df_rusak = data['df_rusak']
        df_rugi = data['df_rugi']

        # solution to strange bottom stacked bar plot
        bottom_rusak = data['bottom_rusak']
        bottom_rugi = data['bottom_rugi']

        # bar plot configuration
        len_index = len(df_rusak.values[0])
        bar_width = 0.2
        index = np.arange(len_index) + 0.1

        # kerusakan
        ax_rusak_title = self.fig.add_axes(
            [0.1, 0.84, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_rusak_bar = self.fig.add_axes([0.18,0.475,0.5,0.34], frame_on=True)

        ax_rusak_title.text(0, 0.25, subtitle[0], fontproperties=font_prop['normal_font'])

        for i in xrange(len(df_rusak)):
            if (i == 0):
                ax_rusak_bar.bar(
                    index, df_rusak.ix[i].values,
                    bar_width, color=self.colors[i],
                    label=df_rusak.index[i])
            else:
                ax_rusak_bar.bar(
                    index, df_rusak.ix[i].values,
                    bar_width, color=self.colors[i],
                    bottom=bottom_rusak.ix[i-1].values,
                    label=df_rusak.index[i])
            plt.xticks(index + 0.1, df_rusak.axes[1], fontproperties=font_prop['x_tick'])

        y_format = ticker.FuncFormatter('{:,.0f}'.format)
        ax_rusak_bar.yaxis.set_major_formatter(y_format)
        # set_ylim mitigate ugly graph when all loss data equal to zero
        if df_rusak.sum().sum() == 0.0:
            ax_rusak_bar.set_ylim(bottom=0, top=7)
        ax_rusak_bar.legend(fontsize='xx-small', loc=(1.03,0))

        # kerugian
        ax_rugi_title = self.fig.add_axes(
            [0.1, 0.43, 0.8, 0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_rugi_bar = self.fig.add_axes([0.18,0.065,0.5,0.34], frame_on=True)

        ax_rugi_title.text(0, 0.25, subtitle[1], fontproperties=font_prop['normal_font'])

        for i in xrange(len(df_rusak)):
            if (i == 0):
                ax_rugi_bar.bar(
                    index, df_rugi.ix[i].values,
                    bar_width, color=self.colors[i],
                    label=df_rugi.index[i])
            else:
                ax_rugi_bar.bar(
                    index, df_rugi.ix[i].values,
                    bar_width, color=self.colors[i],
                    bottom=bottom_rugi.ix[i-1].values,
                    label=df_rugi.index[i])
            plt.xticks(index + 0.1, df_rugi.axes[1], fontproperties=font_prop['x_tick'])

        ax_rugi_bar.yaxis.set_major_formatter(y_format)
        # set_ylim mitigate ugly graph when all loss data equal to zero
        if df_rugi.sum().sum() == 0.0:
            ax_rugi_bar.set_ylim(bottom=0, top=7)
        ax_rugi_bar.legend(fontsize='xx-small', loc=(1.03,0))

    def page_asuransi(self, data):

        """
        Membuat tabel dan grafik batang untuk dala asuransi pada halaman terakhir

        :param data: data untuk halaman tersebut
        """

        # data
        asuransi_rusak = data['asuransi_rusak']
        asuransi_rugi = data['asuransi_rugi']
        asuransi_detil = data['asuransi_detil']
        total_rusak = data['total_rusak']
        total_rugi = data['total_rugi']
        total_detil = data['total_detil']
        df_table = data['df_table']
        bottom_rugi = data['bottom_rugi']

        # teks kerusakan dan kerugian asuransi

        # tabel kerusakan asuransi
        cell = CraftCell(0.05, 0.78, height_cell=0.015, width_cell=0.11)

        # row 0
        cell.insert_text_blues(self.fig, 0, 0, '')
        cell.insert_text_blues(self.fig, 0, 1, '')
        cell.insert_text_blues(self.fig, 0, 2, '')
        cell.insert_text_blues(self.fig, 0, 3, '')
        cell.insert_text_blues(self.fig, 0, 4, 'KERUSAKAN')
        cell.insert_text_blues(self.fig, 0, 5, '')
        cell.insert_text_blues(self.fig, 0, 6, '')
        cell.insert_text_blues(self.fig, 0, 7, 'TOTAL')

        # row 1
        cell.insert_text_blues(self.fig, 1, 0, 'SUBSEKTOR', underline=True)
        cell.insert_text_blues(self.fig, 1, 1, 'ASET', underline=True)
        cell.insert_text_blues(self.fig, 1, 2, 'JAKUT', underline=True)
        cell.insert_text_blues(self.fig, 1, 3, 'JAKSEL', underline=True)
        cell.insert_text_blues(self.fig, 1, 4, 'JAKPUS', underline=True)
        cell.insert_text_blues(self.fig, 1, 5, 'JAKBAR', underline=True)
        cell.insert_text_blues(self.fig, 1, 6, 'JAKTIM', underline=True)
        cell.insert_text_blues(self.fig, 1, 7, '', underline=True)

        # row 2
        cell.insert_text(self.fig, 2, 0, 'FINANSIAL', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 1, 'ASURANSI', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 2, asuransi_rusak.JAKUT, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 3, asuransi_rusak.JAKSEL, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 4, asuransi_rusak.JAKPUS, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 5, asuransi_rusak.JAKBAR, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 6, asuransi_rusak.JAKTIM, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 7, asuransi_rusak.TOTAL, jenis='angka', underline=True, width=2.5)

        # row 3
        cell.insert_text(self.fig, 3, 0, 'TOTAL', underline=True)
        cell.insert_text(self.fig, 3, 1, '', underline=True)
        cell.insert_text(self.fig, 3, 2, total_rusak.JAKUT, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 3, total_rusak.JAKSEL, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 4, total_rusak.JAKPUS, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 5, total_rusak.JAKBAR, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 6, total_rusak.JAKTIM, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 7, total_rusak.TOTAL, jenis='angka', underline=True)
        cell = None

        # tabel kerugian asuransi
        cell = CraftCell(0.05, 0.7, height_cell=0.015, width_cell=0.11)

        # row 0
        cell.insert_text_oranges(self.fig, 0, 0, '')
        cell.insert_text_oranges(self.fig, 0, 1, '')
        cell.insert_text_oranges(self.fig, 0, 2, '')
        cell.insert_text_oranges(self.fig, 0, 3, '')
        cell.insert_text_oranges(self.fig, 0, 4, 'KERUGIAN')
        cell.insert_text_oranges(self.fig, 0, 5, '')
        cell.insert_text_oranges(self.fig, 0, 6, '')
        cell.insert_text_oranges(self.fig, 0, 7, 'TOTAL')

        # row 1
        cell.insert_text_oranges(self.fig, 1, 0, 'SUBSEKTOR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 1, 'ASET', underline=True)
        cell.insert_text_oranges(self.fig, 1, 2, 'JAKUT', underline=True)
        cell.insert_text_oranges(self.fig, 1, 3, 'JAKSEL', underline=True)
        cell.insert_text_oranges(self.fig, 1, 4, 'JAKPUS', underline=True)
        cell.insert_text_oranges(self.fig, 1, 5, 'JAKBAR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 6, 'JAKTIM', underline=True)
        cell.insert_text_oranges(self.fig, 1, 7, '', underline=True)

        # row 2
        cell.insert_text(self.fig, 2, 0, 'FINANSIAL', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 1, 'ASURANSI', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 2, asuransi_rugi.JAKUT, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 3, asuransi_rugi.JAKSEL, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 4, asuransi_rugi.JAKPUS, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 5, asuransi_rugi.JAKBAR, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 6, asuransi_rugi.JAKTIM, jenis='angka', underline=True, width=2.5)
        cell.insert_text(self.fig, 2, 7, asuransi_rugi.TOTAL, jenis='angka', underline=True, width=2.5)

        # row 3
        cell.insert_text(self.fig, 3, 0, 'TOTAL', underline=True)
        cell.insert_text(self.fig, 3, 1, '', underline=True)
        cell.insert_text(self.fig, 3, 2, total_rugi.JAKUT, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 3, total_rugi.JAKSEL, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 4, total_rugi.JAKPUS, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 5, total_rugi.JAKBAR, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 6, total_rugi.JAKTIM, jenis='angka', underline=True)
        cell.insert_text(self.fig, 3, 7, total_rugi.TOTAL, jenis='angka', underline=True)
        cell = None

        # teks detil kerugian asuransi
        s_subtitle = 'Detail Kerugian Asuransi'
        ax_subtitle = self.fig.add_axes(
            [0.1,0.62,0.8,0.02],
            frame_on=False, xticks=[], yticks=[])
        ax_subtitle.text(0, 0.25, s_subtitle, fontproperties=font_prop['normal_font'])

        # tabel detil kerugian asuransi
        cell = CraftCell(0.04, 0.60, height_cell=0.015, width_cell=0.1)

        # row 0
        cell.insert_text_oranges(self.fig, 0, 0, '')
        cell.insert_text_oranges(self.fig, 0, 1, '')
        cell.insert_text_oranges(self.fig, 0, 2, '')
        cell.insert_text_oranges(self.fig, 0, 3, '')
        cell.insert_text_oranges(self.fig, 0, 4, 'KERUGIAN')
        cell.insert_text_oranges(self.fig, 0, 5, '')
        cell.insert_text_oranges(self.fig, 0, 6, '')
        cell.insert_text_oranges(self.fig, 0, 7, '')
        cell.insert_text_oranges(self.fig, 0, 8, 'TOTAL')

        # row 1
        cell.insert_text_oranges(self.fig, 1, 0, 'SUBSEKTOR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 1, 'ASET', underline=True)
        cell.insert_text_oranges(self.fig, 1, 2, 'ASURANSI', underline=True)
        cell.insert_text_oranges(self.fig, 1, 3, 'JAKUT', underline=True)
        cell.insert_text_oranges(self.fig, 1, 4, 'JAKSEL', underline=True)
        cell.insert_text_oranges(self.fig, 1, 5, 'JAKPUS', underline=True)
        cell.insert_text_oranges(self.fig, 1, 6, 'JAKBAR', underline=True)
        cell.insert_text_oranges(self.fig, 1, 7, 'JAKTIM', underline=True)
        cell.insert_text_oranges(self.fig, 1, 8, '', underline=True)

        # row 2 until last row -1
        for index, row in asuransi_detil.iterrows():
            if row.FLAG == True:
                cell.insert_text(self.fig, index + 2, 0, row.SUBSEKTOR, underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 1, row.ASET, underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 2, row.JENIS_ASURANSI, underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 3, row.JAKUT, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 4, row.JAKSEL, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 5, row.JAKPUS, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 6, row.JAKBAR, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 7, row.JAKTIM, jenis='angka', underline=True, width=2.5)
                cell.insert_text(self.fig, index + 2, 8, row.TOTAL, jenis='angka', underline=True, width=2.5)
            else:
                cell.insert_text(self.fig, index + 2, 0, row.SUBSEKTOR)
                cell.insert_text(self.fig, index + 2, 1, row.ASET)
                cell.insert_text(self.fig, index + 2, 2, row.JENIS_ASURANSI)
                cell.insert_text(self.fig, index + 2, 3, row.JAKUT, jenis='angka')
                cell.insert_text(self.fig, index + 2, 4, row.JAKSEL, jenis='angka')
                cell.insert_text(self.fig, index + 2, 5, row.JAKPUS, jenis='angka')
                cell.insert_text(self.fig, index + 2, 6, row.JAKBAR, jenis='angka')
                cell.insert_text(self.fig, index + 2, 7, row.JAKTIM, jenis='angka')
                cell.insert_text(self.fig, index + 2, 8, row.TOTAL, jenis='angka')

        # last row
        last_row = len(asuransi_detil) + 3
        cell.insert_text(self.fig, last_row, 0, 'TOTAL', underline=True)
        cell.insert_text(self.fig, last_row, 1, '', underline=True)
        cell.insert_text(self.fig, last_row, 2, '', underline=True)
        cell.insert_text(self.fig, last_row, 3, total_detil.JAKUT, jenis='angka', underline=True)
        cell.insert_text(self.fig, last_row, 4, total_detil.JAKSEL, jenis='angka', underline=True)
        cell.insert_text(self.fig, last_row, 5, total_detil.JAKPUS, jenis='angka', underline=True)
        cell.insert_text(self.fig, last_row, 6, total_detil.JAKBAR, jenis='angka', underline=True)
        cell.insert_text(self.fig, last_row, 7, total_detil.JAKTIM, jenis='angka', underline=True)
        cell.insert_text(self.fig, last_row, 8, total_detil.TOTAL, jenis='angka', underline=True)
        cell = None

        # grafik batang kerugian asuransi
        # bar plot configuration
        len_index = len(df_table.values[0])
        bar_width = 0.2
        index = np.arange(len_index) + 0.1

        # begin from below
        ax_rusak_bar = self.fig.add_axes([0.18,0.065,0.5,0.34], frame_on=True)

        for i in xrange(len(df_table)):
            if (i == 0):
                ax_rusak_bar.bar(
                    index, df_table.ix[i].values,
                    bar_width, color=self.colors[i],
                    label=df_table.index[i])
            else:
                ax_rusak_bar.bar(
                    index, df_table.ix[i].values,
                    bar_width, color=self.colors[i],
                    bottom=bottom_rugi.ix[i-1].values,
                    label=df_table.index[i])
            plt.xticks(index + 0.1, df_table.axes[1], fontproperties=font_prop['x_tick'])

        y_format = ticker.FuncFormatter('{:,.0f}'.format)
        ax_rusak_bar.yaxis.set_major_formatter(y_format)
        # set_ylim mitigate ugly graph when all loss data equal to zero
        ax_rusak_bar.set_ylim(bottom=0)
        ax_rusak_bar.legend(fontsize='xx-small', loc=(1.03,0))


    # def page_closing(self, closing):
    #
    #     '''Closing report statement
    #     '''
    #
    #     ax_closing = self.fig.add_axes(
    #         [0.1, 0.1, 0.8, 0.15],
    #         frame_on=False, xticks=[], yticks=[])
    #     ax_closing.text(0, 0.25, closing, fontproperties=font_prop['x_tick'])

##############################################################################

def fix_februari(time_input):

    month = config.time_formatter(time_input, '%d %B %Y', '%B')
    day = config.time_formatter(time_input, '%d %B %Y', '%d')
    year = config.time_formatter(time_input, '%d %B %Y', '%Y')
    if month == 'Pebruari':
        month = 'Februari'
        time_output = day + ' ' + month + ' ' + year
        return time_output
    else:
        return time_input

def report_dala(time_0, time_1, summary, list_subsektor, tipe='auto'):

    """
    Membuat laporan dala dalam bentuk pdf dari hasil perhitungan dala dalam
    bentuk csv di direktori summary

    :param time_0: waktu awal kejadian banjir
    :param time_1: waktu akhir kejadian banjir

    """

    # akses ke konfigurasi
    path = config.Path(time_0, time_1, tipe=tipe)
    image_dir = path.resource_dir

    # membuat halaman pdf
    if not os.path.isdir(path.output_dir):
        os.makedirs(path.output_dir)
    pdf_file = path.output_dir + 'dala_' + time_0 + '_' + time_1 + '.pdf'

    # membuat figure
    fig = PdfFigure(pdf_file)

    # pandas panel summary
    # data
    data_bar_page_1 = summary.get_data_bar_page_1()
    data_table_page_1 = summary.get_data_table_page_1()
    data_bar_page_2 = summary.get_data_bar_page_2()
    data_pie_page_3 = summary.get_data_pie_page_3()
    data_table_page_4_and_5 = summary.get_data_table_page_4_and_5()
    data_bar_page_6 = summary.get_data_bar_page_6()
    data_asuransi = summary.get_data_asuransi()

    # menyetel format waktu ke Indonesia
    import locale
    try:
        locale.setlocale(locale.LC_TIME, 'id_ID.utf8')
    except locale.Error, e:
        print 'error: %s' %e
        sys.exit(1)
    time_0 = config.time_formatter(time_0, '%Y%m%d%H%M%S', '%d %B %Y')
    time_1 = config.time_formatter(time_1, '%Y%m%d%H%M%S', '%d %B %Y')
    time_0 = fix_februari(time_0)
    time_1 = fix_februari(time_1)

    # daftar subtitle
    subtitle = {
        '1' : 'Penilaian Kerusakan dan Kerugian Per Sektor (dalam juta Rupiah)',
        '2' : 'Penilaian Kerusakan dan Kerugian Per Subsektor (dalam juta Rupiah)',
        '3' : ('Kerusakan per Subsektor (dalam juta Rupiah)',
            'Kerugian Per Subsektor (dalam juta Rupiah)',),
        '4' : 'Kerusakan per Subsektor (dalam juta Rupiah)',
        '5' : 'Kerugian Per Subsektor (dalam juta Rupiah)',
        '6' : 'Kerusakan dan Kerugian Per Wilayah (dalam juta Rupiah)',
        'PERTANIAN' : ('Kerusakan Subsektor Pertanian (dalam juta Rupiah)',
            'Kerugian Subsektor Pertanian (dalam juta Rupiah)',),
        'PERDAGANGAN' : ('Kerusakan Subsektor Perdagangan (dalam juta Rupiah)',
            'Kerugian Subsektor Perdagangan (dalam juta Rupiah)',),
        'INDUSTRI' : ('Kerusakan Subsektor Industri (dalam juta Rupiah)',
            'Kerugian Subsektor Industri (dalam juta Rupiah)',),
        'PARIWISATA' : ('Kerusakan Subsektor Pariwisata (dalam juta Rupiah)',
            'Kerugian Subsektor Pariwisata (dalam juta Rupiah)',),
        'PERUMAHAN' : ('Kerusakan Subsektor Perumahan (dalam juta Rupiah)',
            'Kerugian Subsektor Perumahan (dalam juta Rupiah)',),
        'KESEHATAN' : ('Kerusakan Subsektor Kesehatan (dalam juta Rupiah)',
            'Kerugian Subsektor Kesehatan (dalam juta Rupiah)',),
        'PENDIDIKAN' : ('Kerusakan Subsektor Pendidikan (dalam juta Rupiah)',
            'Kerugian Subsektor Pendidikan (dalam juta Rupiah)',),
        'TRANSPORTASI' : ('Kerusakan Subsektor Transportasi (dalam juta Rupiah)',
            'Kerugian Subsektor Transportasi (dalam juta Rupiah)',),
        'TELEKOMUNIKASI' : ('Kerusakan Subsektor Telekomunikasi (dalam juta Rupiah)',
            'Kerugian Subsektor Telekomunikasi (dalam juta Rupiah)',),
        'ENERGI' : ('Kerusakan Subsektor Energi (dalam juta Rupiah)',
            'Kerugian Subsektor Energi (dalam juta Rupiah)',),
        'AIR BERSIH DAN SANITASI' : ('Kerusakan Subsektor Air Bersih dan Sanitasi (dalam juta Rupiah)',
            'Kerugian Subsektor Air Bersih dan Sanitasi (dalam juta Rupiah)',),
        'PEMERINTAHAN' : ('Kerusakan Subsektor Pemerintahan (dalam juta Rupiah)',
            'Kerugian Subsektor Pemerintahan (dalam juta Rupiah)',),
        'LINGKUNGAN' : ('Kerusakan Subsektor Lingkungan (dalam juta Rupiah)',
            'Kerugian Subsektor Lingkungan (dalam juta Rupiah)',),
        'FINANSIAL' : ('Kerusakan Subsektor Finansial (dalam juta Rupiah)',
            'Kerugian Subsektor Finansial (dalam juta Rupiah)',),
        'AGAMA' : ('Kerusakan Subsektor Agama (dalam juta Rupiah)',
            'Kerugian Subsektor Agama (dalam juta Rupiah)'),
        'ASURANSI' : 'Kerusakan dan Kerugian Asuransi',
    }

    # page 1
    fig.page_title(image_dir)
    fig.page_date(time_0, time_1)
    fig.page_subtitle(subtitle['1'])
    fig.page_half_table(data_table_page_1)
    fig.page_bar(data_bar_page_1)
    fig.write_pdf()
    fig.clear_figure()

    # page 2
    fig.page_title(image_dir)
    fig.page_half_bar(data_bar_page_2, subtitle['2'])
    fig.write_pdf()
    fig.clear_figure()

    # page 3
    fig.page_title(image_dir)
    fig.page_half_pie(data_pie_page_3, subtitle['3'])
    fig.write_pdf()
    fig.clear_figure()

    # page 4
    fig.page_title(image_dir)
    fig.page_subtitle(subtitle['4'], page_1=False)
    fig.page_full_table(data_table_page_4_and_5, 'KERUSAKAN')
    fig.write_pdf()
    fig.clear_figure()

    # page 5
    fig.page_title(image_dir)
    fig.page_subtitle(subtitle['5'], page_1=False)
    fig.page_full_table(data_table_page_4_and_5, 'KERUGIAN')
    fig.write_pdf()
    fig.clear_figure()

    # page 6
    fig.page_title(image_dir)
    fig.page_summary_region(data_bar_page_6, subtitle['6'])
    fig.write_pdf()
    fig.clear_figure()

    for subsektor in list_subsektor:
        # page 7 until last page -1
        data_bar_per = summary.get_data_bar_per(subsektor)
        fig.page_title(image_dir)
        fig.page_region_bar(data_bar_per, subtitle[subsektor])
        fig.write_pdf()
        fig.clear_figure()

    # last page (finansial asuransi terpisah)
    fig.page_title(image_dir)
    fig.page_date(time_0, time_1)
    fig.page_subtitle(subtitle['ASURANSI'])
    fig.page_asuransi(data_asuransi)
    fig.write_pdf()
    fig.clear_figure()

    # finish
    fig.finish_pdf()

################################################################################
