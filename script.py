from benchmarks import partialsolvers_benchmark as bench

# print "worstcase"

# print "worst case lam 1-4-7-10 DirFixWP V1"
# worst case lam 1-4-7-10 DirFixWP V1
# bench.benchmark_worst_case_wp(22, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = False, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_Dir_v1", save_res = True, path_res="Resultats/worstcase/res_Dir_v1", prt = False)

# print "worst case lam 1-4-7-10 DirFixWP V2"
# worst case lam 1-4-7-10 DirFixWP V2
# bench.benchmark_worst_case_wp(22, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = True, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_Dir_v2", save_res = True, path_res="Resultats/worstcase/res_Dir_v2", prt = False)

print "worst case lam 1-4-7-10 FixWP V1"
# worst case lam 1-4-7-10 FixWP V1
bench.benchmark_worst_case_wp(22, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = False, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_fix_v1", save_res = True, path_res="Resultats/worstcase/res_fix_v1", prt = False)

print "worst case lam 1-4-7-10 FixWP V2"
# worst case lam 1-4-7-10 FixWP V2
bench.benchmark_worst_case_wp(22, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = True, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_fix_v2", save_res = True, path_res="Resultats/worstcase/res_fix_v2", prt = False)

# print "worst case wc"
# #worst case wc
# bench.benchmark_worst_case_wc(22, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_wc", save_res = True, path_res = "Resultats/worstcase/res_wc", prt = False)

# print "Ladder"

# print "ladder lam 1-4-7-10 DirFixWP V1"
# worst case lam 1-4-7-10 DirFixWP V1
# bench.benchmark_ladder_wp(101, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = False, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_Dir_v1", save_res = True, path_res="Resultats/ladder/res_Dir_v1", prt = False)

# print "ladder lam 1-4-7-10 DirFixWP V2"
# worst case lam 1-4-7-10 DirFixWP V2
# bench.benchmark_ladder_wp(101, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = True, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_Dir_v2", save_res = True, path_res="Resultats/ladder/res_Dir_v2", prt = False)

# print "ladder lam 1-4-7-10 FixWP V1"
# worst case lam 1-4-7-10 FixWP V1
# bench.benchmark_ladder_wp(101, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = False, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_fix_v1", save_res = True, path_res="Resultats/ladder/res_fix_v1", prt = False)

# print "ladder lam 1-4-7-10 FixWP V2"
# ladder lam 1-4-7-10 FixWP V2
# bench.benchmark_ladder_wp(101, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = True, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_fix_v2", save_res = True, path_res="Resultats/ladder/res_fix_v2", prt = False)

# print "ladder wc"
# ladder wc
# bench.benchmark_ladder_wc(101, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_wc", save_res = True, path_res = "Resultats/ladder/res_wc", prt = False)

# print "worst case wc"
# #worst case wc
# bench.benchmark_worst_case_wc(40, iterations=3, step=3, plot=True, path="Resultats/worstcase/plot_wc2", save_res = True, path_res = "Resultats/worstcase/res_wc2", prt = False)

# print "Ladder"

# print "ladder lam 1-4-7-10 DirFixWP V1"
# # worst case lam 1-4-7-10 DirFixWP V1
# bench.benchmark_ladder_wp(1000, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = False, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_Dir_v1_1000", save_res = True, path_res="Resultats/ladder/res_Dir_v1_1000", prt = False)

# print "ladder lam 1-4-7-10 DirFixWP V2"
# # worst case lam 1-4-7-10 DirFixWP V2
# bench.benchmark_ladder_wp(1000, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = True, v2 = True, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_Dir_v2_1000", save_res = True, path_res="Resultats/ladder/res_Dir_v2_1000", prt = False)

# print "ladder lam 1-4-7-10 FixWP V1"
# # worst case lam 1-4-7-10 FixWP V1
# bench.benchmark_ladder_wp(1000, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = False, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_fix_v1_1000", save_res = True, path_res="Resultats/ladder/res_fix_v1_1000", prt = False)

# print "ladder lam 1-4-7-10 FixWP V2"
# # ladder lam 1-4-7-10 FixWP V2
# bench.benchmark_ladder_wp(1000, start_lambda = 1, end_lambda = 10, step_lambda = 3, dir = False, v2 = True, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_fix_v2_1000", save_res = True, path_res="Resultats/ladder/res_fix_v2_1000", prt = False)

# print "ladder wc"
# # ladder wc
# bench.benchmark_ladder_wc(1000, iterations=3, step=10, plot=True, path="Resultats/ladder/plot_wc_1000", save_res = True, path_res = "Resultats/ladder/res_wc_1000", prt = False)

# # random lam 5, 5 essais, taille 1 - 200, step 10
# print "random lam 5, 5 essais, taille 1 - 200, step 10"
# #    dirfixwp v1
# print "dirfixwp v1"
# bench.launch_random_wp(200, 5, lam=1, dir = True, v2 = False, plot = True, path="Resultats/random/plot_dirwp1_lam1", save_res = True, path_res = "Resultats/random/res_dirwp1_lam1")
# #   dirfixwp v2
# print "dirfixwp v2"
# bench.launch_random_wp(200, 5, lam=1, dir = True, v2 = True, plot = True, path="Resultats/random/plot_dirwp2_lam1", save_res = True, path_res = "Resultats/random/res_dirwp2_lam1")
# #   fixwp v1
# print "fixwp v1"
# bench.launch_random_wp(200, 5, lam=1, dir = False, v2 = False, plot = True, path="Resultats/random/plot_wp1_lam1", save_res = True, path_res = "Resultats/random/res_wp1_lam1")

# #   fixwp v2
# bench.launch_random_wp(200, 5, lam=1, dir = False, v2 = True, plot = True, path="Resultats/random/plot_wp2_lam1", save_res = True, path_res = "Resultats/random/res_wp2_lam1")

# #   winningcore
# bench.launch_random_wc(200, 20, step = 10, plot=True, path="Resultats/random/plot_wc_1000", save_res = True, path_res = "Resultats/random/res_wc_1000")