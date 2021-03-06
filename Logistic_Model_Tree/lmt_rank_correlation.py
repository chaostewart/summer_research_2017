
import mysql.connector
import os

from sshtunnel import SSHTunnelForwarder

with SSHTunnelForwarder(('rcg-linux-ts1.rcg.sfu.ca', 22),
                        ssh_username = "cla315",
                        ssh_password="Life5uck5!",
                        remote_bind_address=('cs-oschulte-01.cs.sfu.ca', 3306)) as server:

    #connect to database server
    mydb = mysql.connector.connect(host='127.0.0.1',
                                   port = server.local_bind_port,
                                   user='root', passwd='joinbayes',
                                   db='chao_draft')
    cursor = mydb.cursor()

    for year in [2001, 2002, 2007, 2008]:
        cursor.execute("""Drop view if exists chao_draft.cal_lmt_rank_corr_CSS_null_norm_%s_view;""" % str(year))
        mydb.commit()
        cursor.execute("""Create view chao_draft.cal_lmt_rank_corr_CSS_null_norm_%s_view as
                    SELECT id, PlayerName, DraftYear, rank_sum_7yr_GP, 
                    skaters_overall, pow(skaters_overall-rank_sum_7yr_GP, 2) as di2_overall,          
                    rank_lmt_notie, pow(rank_lmt_notie - rank_sum_7yr_GP, 2) as di2_lmt_notie,
                    rank_lmt_tied, pow(rank_lmt_tied - rank_sum_7yr_GP, 2) as di2_lmt_tied
                  FROM chao_draft.union_all_ranks_with_lmt_view
                  WHERE DraftYear = %s;""" % (str(year), str(year)))
        mydb.commit()

        cursor.execute("""select count(*), sum(di2_overall), sum(di2_lmt_notie), sum(di2_lmt_tied)
                        from chao_draft.cal_lmt_rank_corr_CSS_null_norm_%s_view;""" % str(year))
        #mydb.commit()
        row = cursor.fetchone()
        print str(row)
        total_num = int(row[0])
        overall_rank_corr = float(1 - 6 * float(row[1])/(float(total_num) * (pow(total_num, 2) - 1)))
        print 'Overall rank corr. is ' + str(overall_rank_corr)
        lmt_rank_notie_corr = float(1 - 6 * float(row[2]) / (float(total_num) * (pow(total_num, 2) - 1)))
        print 'lmt_rank_notie rank corr. is ' + str(lmt_rank_notie_corr)
        lmt_rank_tied_corr = float(1 - 6 * float(row[3]) / (float(total_num) * (pow(total_num, 2) - 1)))
        print 'lmt_rank_tied corr. is ' + str(lmt_rank_tied_corr)

    cursor.close()
    print "Rank table has been created."
