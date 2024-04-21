from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

graphviz = GraphvizOutput()
graphviz.output_file = 'basicdemo.pdf'

with PyCallGraph(output=graphviz):
    import cntv
    id = '2024/04/18/VIDE5n5Lbl1QoCD2K922xnS8240418'
    keyword = '中东'
    cntv.get_video_info(id, 'ID')