from Plotter_API import plotter


P = plotter()

F = P.read('API_file.txt')

P.load('test.rplt')
P.restore()

P.add_graph(F,'time','X')
# P.info()

# P.create_graph(F,'time','Z')
# P.add_graph(F,'time','Y')
# P.save()
# p.test()