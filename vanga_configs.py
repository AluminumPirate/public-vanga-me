__DETAILED_PRINTING__ = True

db_filename = "database/test_threading.db"

yfinance_table_name = 'yfinance_data'
prediction_accuracy_table_name = "prediction_accuracy"
stories_data_table_name = "stories_data"
prediction_last_x_time_table_name = "last_prediction_accuracy"

future_prediction_default_days_to_subtract = 7
future_prediction_default_last_hours_to_subtract = 12
predictions_accuracy_default_days_to_subtract = 5

compound_sentiment_threshold = -0.5
basic_search_term_google_and_yf_ticker_name = [['Bitcoin', 'BTC-USD'], ['Ethereum', 'ETH-USD'],
                                               ['BinanceCoin', 'BNB-USD'],
                                               ['Tether', 'USDT-USD'], ['Cardano ', 'ADA-USD'],
                                               ['Solana', 'SOL1-USD'],
                                               ['XRP', 'XRP-USD'], ['Polkadot', 'DOT1-USD'],
                                               ['USDCoin', 'USDC-USD'],
                                               ['"hex coin"', 'HEX-USD'], ['Dogecoin', 'DOGE-USD'],
                                               ['Avalanche', 'AVAX-USD']]
