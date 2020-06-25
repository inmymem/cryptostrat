import os

st1_limit = 5000 #5000
st2_limit = 10000 #10000
st0_and_st1_one_transaction_limit = 2000#also applies to st0

if (os.environ['DEBUG'] == 'True'):
    st1_limit = 50 #5000
    st2_limit = 100 #10000
    st0_and_st1_one_transaction_limit = 20