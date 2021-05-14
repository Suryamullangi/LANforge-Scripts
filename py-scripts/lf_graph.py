#!/usr/bin/env python3
'''
NAME: lf_graph.py

PURPOSE: 
Common Library for generating graphs for LANforge output

SETUP:  
/lanforge/html-reports directory needs to be present or output generated in local file

EXAMPLE:  
see: /py-scritps/lf_report_test.py for example

COPYWRITE
    Copyright 2021 Candela Technologies Inc
    License: Free to distribute and modify. LANforge systems must be licensed.

INCLUDE_IN_README
'''

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas as pd
import pdfkit
import math
from matplotlib.colors import ListedColormap


# internal candela references included during intial phases, to be deleted at future date

# graph reporting classes
class lf_bar_graph():
    def __init__(self, _data_set=[[30, 55, 69, 37], [45, 67, 34, 22], [22, 45, 12, 34]],
                 _xaxis_name="x-axis",
                 _yaxis_name="y-axis",
                 _xaxis_categories=[1, 2, 3, 4],
                 _graph_image_name="image_name",
                 _label=["bi-downlink", "bi-uplink", 'uplink'],
                 _color=None,
                 _bar_width=0.25,
                 _color_edge='grey',
                 _font_weight='bold',
                 _color_name=['lightcoral', 'darkgrey', 'r', 'g', 'b', 'y'],
                 _figsize=(10, 5),
                 _dpi=96):

        self.data_set = _data_set
        self.xaxis_name = _xaxis_name
        self.yaxis_name = _yaxis_name
        self.xaxis_categories = _xaxis_categories
        self.graph_image_name = _graph_image_name
        self.label = _label
        self.color = _color
        self.bar_width = _bar_width
        self.color_edge = _color_edge
        self.font_weight = _font_weight
        self.color_name = _color_name
        self.figsize = _figsize

    def build_bar_graph(self):
        if self.color is None:
            i = 0
            self.color = []
            for col in self.data_set:
                self.color.append(self.color_name[i])
                i = i + 1

        fig = plt.subplots(figsize=self.figsize)
        i = 0
        for data in self.data_set:
            if i > 0:
                br = br1
                br2 = [x + self.bar_width for x in br]
                plt.bar(br2, self.data_set[i], color=self.color[i], width=self.bar_width,
                        edgecolor=self.color_edge, label=self.label[i])
                br1 = br2
                i = i + 1
            else:
                br1 = np.arange(len(self.data_set[i]))
                plt.bar(br1, self.data_set[i], color=self.color[i], width=self.bar_width,
                        edgecolor=self.color_edge, label=self.label[i])
                i = i + 1
        plt.xlabel(self.xaxis_name, fontweight='bold', fontsize=15)
        plt.ylabel(self.yaxis_name, fontweight='bold', fontsize=15)
        """plt.xticks([r + self.bar_width for r in range(len(self.data_set[0]))],
                   self.xaxis_categories)"""
        plt.xticks(np.arange(0, len(self.xaxis_categories), step=5))
        plt.legend()

        fig = plt.gcf()
        plt.savefig("%s.png" % self.graph_image_name, dpi=96)
        plt.close()
        print("{}.png".format(self.graph_image_name))

        return "%s.png" % self.graph_image_name


class lf_scatter_graph():
    def __init__(self,
                 _x_data_set=["sta0 ", "sta1", "sta2", "sta3"],
                 _y_data_set=[[30, 55, 69, 37]],
                 _values=None,
                 _xaxis_name="x-axis",
                 _yaxis_name="y-axis",
                 _label=["num1", "num2"],
                 _graph_image_name="image_name",
                 _color=["r", "y"],
                 _figsize=(9, 4)):
        self.x_data_set = _x_data_set
        self.y_data_set = _y_data_set
        self.xaxis_name = _xaxis_name
        self.yaxis_name = _yaxis_name
        self.figsize = _figsize
        self.graph_image_name = _graph_image_name
        self.color = _color
        self.label = _label
        self.values = _values

    def build_scatter_graph(self):
        if self.color is None:
            self.color = ["orchid", "lime", "aquamarine", "royalblue", "darkgray", "maroon"]
        fig = plt.subplots(figsize=self.figsize)
        if self.values is None:
            plt.scatter(self.x_data_set, self.y_data_set[0], color=self.color[0], label=self.label[0])
            if len(self.y_data_set) > 1:
                for i in range(1, len(self.y_data_set)):
                    plt.scatter(self.x_data_set, self.y_data_set[i], color=self.color[i], label=self.label[i])
            plt.xlabel(self.xaxis_name, fontweight='bold', fontsize=15)
            plt.ylabel(self.yaxis_name, fontweight='bold', fontsize=15)
            plt.gcf().autofmt_xdate()
            plt.legend()
        else:
            colours = ListedColormap(self.color)
            scatter = plt.scatter(self.x_data_set, self.y_data_set, c=self.values, cmap=colours)
            plt.xlabel(self.xaxis_name, fontweight='bold', fontsize=15)
            plt.ylabel(self.yaxis_name, fontweight='bold', fontsize=15)
            plt.gcf().autofmt_xdate()
            plt.legend(handles=scatter.legend_elements()[0], labels=self.label)
        plt.savefig("%s.png" % self.graph_image_name, dpi=96)
        plt.close()
        print("{}.png".format(self.graph_image_name))

        return "%s.png" % self.graph_image_name


class lf_stacked_graph():
    def __init__(self,
                 _data_set=[[1, 2, 3, 4], [1, 1, 1, 1], [1, 1, 1, 1]],
                 _xaxis_name="Stations",
                 _yaxis_name="Numbers",
                 _label=['Success', 'Fail'],
                 _graph_image_name="image_name",
                 _color=["b", "g"],
                 _figsize=(9, 4)):
        self.data_set = _data_set  # [x_axis,y1_axis,y2_axis]
        self.xaxis_name = _xaxis_name
        self.yaxis_name = _yaxis_name
        self.figsize = _figsize
        self.graph_image_name = _graph_image_name
        self.label = _label
        self.color = _color

    def build_stacked_graph(self):
        fig = plt.subplots(figsize=self.figsize)
        if self.color is None:
            self.color = ["darkred", "tomato", "springgreen", "skyblue", "indigo", "plum"]
        plt.bar(self.data_set[0], self.data_set[1], color=self.color[0])
        plt.bar(self.data_set[0], self.data_set[2], bottom=self.data_set[1], color=self.color[1])
        if len(self.data_set) > 3:
            for i in range(3, len(self.data_set)):
                plt.bar(self.data_set[0], self.data_set[i],
                        bottom=np.array(self.data_set[i - 2]) + np.array(self.data_set[i - 1]), color=self.color[i - 1])
        plt.xlabel(self.xaxis_name)
        plt.ylabel(self.yaxis_name)
        plt.legend(self.label)
        plt.savefig("%s.png" % (self.graph_image_name), dpi=96)
        plt.close()
        print("{}.png".format(self.graph_image_name))

        return "%s.png" % (self.graph_image_name)


class lf_horizontal_stacked_graph():
    def __init__(self,
                 _seg=2,
                 _yaxis_set=('A', 'B'),
                 _xaxis_set1=[12, 0, 0, 16, 15],
                 _xaxis_set2=[23, 34, 23, 0],
                 _unit="%",
                 _xaxis_name="Stations",
                 _label=['Success', 'Fail'],
                 _graph_image_name="image_name",
                 _color=["success", "Fail"],
                 _figsize=(9, 4)):
        self.unit = _unit
        self.seg = _seg
        self.xaxis_set1 = _xaxis_set1
        self.xaxis_set2 = _xaxis_set2
        self.yaxis_set = _yaxis_set
        self.xaxis_name = _xaxis_name
        self.figsize = _figsize
        self.graph_image_name = _graph_image_name
        self.label = _label
        self.color = _color

    def build_horizontal_stacked_graph(self):
        def sumzip(items):
            return [sum(values) for values in zip(items)]

        fig, ax = plt.subplots(figsize=self.figsize)

        n = self.seg
        values1 = self.xaxis_set1
        values2 = self.xaxis_set2

        ind = np.arange(n) + .15
        width = 0.3

        rects1 = plt.barh(ind, values1, width, color=self.color[0], label=self.label[0])
        rects2 = plt.barh(ind, values2, width, left=sumzip(values1), color=self.color[1], label=self.label[1])

        extra_space = 0.15
        ax.set_yticks(ind + width - extra_space)
        ax.set_yticklabels(self.yaxis_set)
        ax.yaxis.set_tick_params(length=0, labelbottom=True)

        for i, v in enumerate(values1):
            if v != 0:
                plt.text(v * 0.45, i + .145, "%s%s" % (v, self.unit), color='white', fontweight='bold', fontsize=10,
                         ha='center', va='center')

        for i, v in enumerate(values2):
            if v != 0:
                plt.text(v * 0.45 + values1[i], i + .145, "%s%s" % (v, self.unit), color='white', fontweight='bold',
                         fontsize=10,
                         ha='center', va='center')

        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.legend(loc='upper right')
        plt.savefig("%s.png" % self.graph_image_name, dpi=96)
        plt.close()
        print("{}.png".format(self.graph_image_name))

        return "%s.png" % self.graph_image_name


# Unit Test
if __name__ == "__main__":
    output_html_1 = "graph_1.html"
    output_pdf_1 = "graph_1.pdf"

    # test build_bar_graph with defaults
    graph = lf_bar_graph()
    graph_html_obj = """
        <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + "%s" % (graph.build_bar_graph()) + """ border='1' />
        <br><br>
        """
    # 
    test_file = open(output_html_1, "w")
    test_file.write(graph_html_obj)
    test_file.close()

    # write to pdf
    # write logic to generate pdf here
    # wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
    # sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
    options = {"enable-local-file-access": None}  # prevent eerror Blocked access to file
    pdfkit.from_file(output_html_1, output_pdf_1, options=options)

    # test build_bar_graph setting values
    dataset = [[45, 67, 34, 22], [22, 45, 12, 34], [30, 55, 69, 37]]
    x_axis_values = [1, 2, 3, 4]

    output_html_2 = "graph_2.html"
    output_pdf_2 = "graph_2.pdf"

    # test build_bar_graph with defaults
    graph = lf_bar_graph(_data_set=dataset,
                         _xaxis_name="stations",
                         _yaxis_name="Throughput 2 (Mbps)",
                         _xaxis_categories=x_axis_values,
                         _graph_image_name="Bi-single_radio_2.4GHz",
                         _label=["bi-downlink", "bi-uplink", 'uplink'],
                         _color=None,
                         _color_edge='red')
    graph_html_obj = """
        <img align='center' style='padding:15;margin:5;width:1000px;' src=""" + "%s" % (graph.build_bar_graph()) + """ border='1' />
        <br><br>
        """
    # 
    test_file = open(output_html_2, "w")
    test_file.write(graph_html_obj)
    test_file.close()

    # write to pdf
    # write logic to generate pdf here
    # wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox_0.12.6-1.focal_amd64.deb
    # sudo apt install ./wkhtmltox_0.12.6-1.focal_amd64.deb
    options = {"enable-local-file-access": None}  # prevent eerror Blocked access to file
    pdfkit.from_file(output_html_2, output_pdf_2, options=options)
