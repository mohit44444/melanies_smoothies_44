# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders :cup_with_straw:")
st.write(
    """Orders that need to be filled.
    """
)


session = get_active_session()

my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")=="FALSE").collect()
if my_dataframe:
 editable_df = st.data_editor(my_dataframe)
 lis1=[]
 for row in editable_df:
  if row[1]:
   lis1.append('update smoothies.public.orders set order_filled='+"'TRUE'"+' where order_uid='+str(row[0]))

 submitted=st.button('Submit')
 if submitted:
   try: 
    for sql in lis1:
        session.sql(sql).collect()
    st.success('Someone clicked the button', icon = '👍')
   except:
       st.write('Something went wrong.')
else:
    st.success('There are no pending order right now', icon = '👍')