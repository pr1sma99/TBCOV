import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd


def read_table(file_path, n, read_all=False):
    dtypes = {'tweet_id': 'Int64', 'user_id': 'Int64', 'retweeted_id': 'Int64',
              'quoted_id': 'Int64', 'in_reply_to_id': 'Int64'}
    cols = None if read_all else ['tweet_id', 'date_time', 'user_id', 'retweeted_id', 'quoted_id', 'in_reply_to_id']
    covid_df = pd.read_csv(file_path, sep='\t', nrows=n, dtype=dtypes, usecols=cols,
                           index_col='tweet_id', parse_dates=['date_time'])
    return covid_df


def df_summary(df):
    print(df.dtypes)
    print(df.describe(include='all').to_string())


def get_graph(df):
    e = []
    for link_id in ['retweeted_id', 'quoted_id', 'in_reply_to_id']:
        link = df[df[link_id].notna()]
        for index, row in link.iterrows():
            if row[link_id] in df.index:
                if row.user_id != df.loc[row[link_id], 'user_id']:
                    e.append((row.user_id, df.loc[row[link_id], 'user_id']))
    g = nx.MultiDiGraph(e)
    nx.set_node_attributes(g, nx.degree_centrality(g), "deg_cent")
    nx.set_node_attributes(g, nx.pagerank(g), "page_rank")
    return g


def get_subgraph(g, pr):
    g_sub = g.subgraph(nodes=[n for n, d in g.nodes(data=True) if d['page_rank'] > pr])
    print(sorted(nx.get_node_attributes(g_sub, "page_rank").items(), key=lambda x: x[1], reverse=True))
    print(sorted(nx.get_node_attributes(g_sub, "deg_cent").items(), key=lambda x: x[1], reverse=True))
    return g_sub


def get_connected_components(g):
    S = [g.subgraph(c).copy() for c in nx.connected_components(nx.Graph(g))]
    S.sort(reverse=True, key=len)
    return S


def graph_summary(g):
    plt.figure()
    plt.subplot(211)
    plt.hist(nx.degree_histogram(g))
    plt.subplot(212)
    plt.hist(list(nx.get_node_attributes(g, "page_rank").values()))
    plt.show()


def plot_graph(g):
    plt.figure()
    ns = [v * 10000 + 100 for v in nx.get_node_attributes(g, "page_rank").values()]
    nx.draw(g, node_size=ns, alpha=0.9)
    plt.show()


if __name__ == '__main__':
    uk_feb = read_table('united_kingdom_01.tsv', 1300000, read_all=True)
    uk_feb = uk_feb[uk_feb.date_time.dt.month == 2]
    df_summary(uk_feb)
    g_feb = get_graph(uk_feb)
    g_feb_sub = get_subgraph(g_feb, 0.001)
    graph_summary(g_feb)
    plot_graph(g_feb_sub)
