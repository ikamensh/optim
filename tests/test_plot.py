from utils.plot import Metric, plot_group


def test_plot_group():
    m = Metric('x', 'y')
    m.add_many(1, [1, 2, 3])
    m.add_record(2, 4)
    m.add_many(4, [5, 6, 12])

    m2 = Metric('x', 'y')
    m2.add_many(1, [4, 3, 5])
    m2.add_record(2, 5)
    m2.add_record(2, 9)
    m2.add_many(4, [5, 6, -1])

    from config import root_dir
    plot_group({'m1': m, 'm2': m2}, root_dir, "bla3")