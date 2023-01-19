import numpy as np
import pandas as pd
import math
from pyproj import Geod

df = pd.read_csv('filein')

g = Geod(ellps='WGS84')

df['dist_real'] = df.apply(lambda row: g.inv(row['bgn_x'], row['bgn_y'], row['end_x'], row['end_y'])[2], axis=1)  
df['dist_simu'] = df.apply(lambda row: g.inv(row['bgn_x'], row['bgn_y'], row['simu_x'], row['simu_y'])[2], axis=1)  
df['azim_real'] = df.apply(lambda row:g.inv(row['bgn_x'], row['bgn_y'], row['end_x'], row['end_y'])[0], axis=1) 
df['azim_simu'] = df.apply(lambda row:g.inv(row['bgn_x'], row['bgn_y'], row['simu_x'], row['simu_y'])[0], axis=1) 
df['v_real'] = df.apply(lambda row: row.dist_real/row.delta_time/24/60/60*100, axis=1)  
df['v_simu'] = df.apply(lambda row: row.dist_simu/row.delta_time/24/60/60*100, axis=1)  
df['vecu_real'] = df.apply( lambda row: (math.sin(math.radians(row.azim_real)) * row.v_real), axis=1 )   
df['vecv_real'] = df.apply( lambda row: (math.cos(math.radians(row.azim_real)) * row.v_real), axis=1 )   
df['vecu_simu'] = df.apply( lambda row: (math.sin(math.radians(row.azim_simu)) * row.v_simu), axis=1 )  
df['vecv_simu'] = df.apply( lambda row: (math.cos(math.radians(row.azim_simu)) * row.v_simu), axis=1 ) 
df['dist_sim2real'] = df.apply(lambda row: g.inv(row['end_x'], row['end_y'], row['simu_x'], row['simu_y'])[2], axis=1)  
df['diff_dist']     = df.apply(lambda row: row.dist_real-row.dist_simu, axis=1)  
df['diff_dist_per'] = df.apply(lambda row: (row.dist_real-row.dist_simu)/row.dist_real, axis=1) 
df['diff_v']     = df.apply(lambda row: row.v_real-row.v_simu, axis=1)  
df['diff_v_per'] = df.apply( lambda row: (row.v_real-row.v_simu)/row.v_real, axis=1 ) 
df['temp'] = df.apply( lambda row: row.azim_real-row.azim_simu, axis=1 ) 
df['diff_azim'] = df.apply( lambda row: 360-row.temp if (row.temp>180) \
                                                            else ( row.temp if ((row.temp>0) & (row.temp<180))\
                                                                else ( 360-math.fabs(row.temp) if (row.temp<-180) \
                                                                    else math.fabs(row.temp) ) ), axis=1 )  
df = df.drop(['temp'], axis = 1)
df['azim_sim2real'] = df.apply(lambda row:g.inv(row['end_x'], row['end_y'], row['simu_x'], row['simu_y'])[0], axis=1) 
df['azim_sim2real_cvt'] = df.apply( lambda row: 360+row.azim_sim2real if (row.azim_sim2real<0) else row.azim_sim2real, axis=1 )
df['diff_vecu'] = df.apply( lambda row: (math.sin(math.radians(row.azim_sim2real_cvt)) * row.dist_sim2real)/row.delta_time/24/60/60*100, axis=1 )  
df['diff_vecv'] = df.apply( lambda row: (math.cos(math.radians(row.azim_sim2real_cvt)) * row.dist_sim2real)/row.delta_time/24/60/60*100, axis=1 ) 
df['vecu_per'] = df.apply( lambda row: row.diff_vecu/math.fabs(row.vecu_real), axis=1 )
df['vecv_per'] = df.apply( lambda row: row.diff_vecv/math.fabs(row.vecv_real), axis=1 )
df = df.drop(['azim_sim2real'], axis = 1)
df = df.drop(['azim_sim2real_cvt'], axis = 1)
df['sin_real'] = df.apply( lambda row: math.sin( math.radians(row.azim_real) ), axis=1 )
df['cos_real'] = df.apply( lambda row: math.cos( math.radians(row.azim_real) ), axis=1 )
df['sin_simu'] = df.apply( lambda row: math.sin( math.radians(row.azim_simu) ), axis=1 )
df['cos_simu'] = df.apply( lambda row: math.cos( math.radians(row.azim_simu) ), axis=1 )

df.to_csv('fileout',index=False)

