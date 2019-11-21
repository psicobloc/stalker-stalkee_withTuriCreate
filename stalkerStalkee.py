import turicreate as tc

checkins = ( tc.SFrame.read_csv( 'loc-gowalla_totalCheckins.txt',
                                 delimiter='\t', header=False )
                .rename( {'X1': 'user_id', 'X2' : 'checkin_ts',
                          'X3': 'lat', 'X4' : 'lon',
                          'X5': 'location_id'} )
  [["user_id", "location_id", "checkin_ts"]] )


chin_ps = ( checkins.join( checkins, on = 'location_id' )
                    .rename( {'checkin_ts'   : 'checkin_ts_ee',
                              'checkin_ts.1' : 'checkin_ts_er',
                              'user_id'      : 'stalkee' ,
                              'user_id.1'    : 'stalker' } ) )

pairs_filtered = chin_ps[ (chin_ps['checkin_ts_ee'] < chin_ps['checkin_ts_er']) &
                                (chin_ps['stalkee'] != chin_ps['stalker']) ]

print (pairs_filtered)

final_result = ( pairs_filtered[['stalkee', 'stalker', 'location_id']]
                    .unique()
                    .groupby( ['stalkee','stalker'] ,
                    operations =  {"location_count" : tc.aggregate.COUNT("location_count") })
                    .topk( 'location_count', k=7 )
                    )

print( final_result )
