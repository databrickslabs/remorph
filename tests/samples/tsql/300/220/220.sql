ADD SENSITIVITY CLASSIFICATION TO
    dbo.sales.price, dbo.sales.discount
    WITH ( LABEL='Highly Confidential', INFORMATION_TYPE='Financial', RANK=CRITICAL )