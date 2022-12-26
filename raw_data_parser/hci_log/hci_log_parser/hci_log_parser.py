

file_name = "hci_log/hci_log_input/zero_value_183F/#2_Abnormal/btsnoop_hci_202201271703.cfa"

cnt = 0;
with open(file_name, 'rb') as fp:
    for block in fp:
        cnt+=1
        if cnt >5: break
        print(block)
