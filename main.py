from vanga_me_core import update_coins_predictions_for_last_x_hours_or_days, get_coin_predictions_history_accuracy, \
    get_monthly_data
from utils.files_util import get_search_term_google_and_yf_ticker_names_from_file, create_vanga_me_db_file
from datetime import datetime, timedelta
import vanga_configs as cfg
import multiprocessing as mlpcs
from threading import Thread
from time import perf_counter

global_term_and_tickers = cfg.basic_search_term_google_and_yf_ticker_name


def get_future_predictions(term_and_tickers, return_dict, days_to_subtract=None, check_x_last_hours=None):
    predictions = None
    try:
        coin_names = []
        for term in term_and_tickers:
            coin_names.append(term[0])

        status, predictions = update_coins_predictions_for_last_x_hours_or_days(coin_names, days_to_subtract,
                                                                                check_x_last_hours)

    except Exception as ex:
        print(f"{ex}")
        return False, f"{ex}"

    for pred in predictions:
        return_dict[pred[0]] = predictions

    return True, predictions


def get_predictions_accuracy(term_and_tickers, days_to_subtract=cfg.predictions_accuracy_default_days_to_subtract):
    try:
        today = datetime.now()
        start_date = today - timedelta(days=days_to_subtract)

        prediction_accuracy = get_coin_predictions_history_accuracy(term_and_tickers,
                                                                    start_date=start_date.strftime("%Y-%m-%d"),
                                                                    # start_date="2014-01-01",
                                                                    end_date=today.strftime("%Y-%m-%d"),
                                                                    multiprocess_enabled=True)
        for prediction in prediction_accuracy.items():
            print(prediction)
        return True, prediction_accuracy
    except Exception as ex:
        print(f"{ex}")
        return False, f"{ex}"


def get_data_for_monthly_accuracy_table_view(terms_and_tickers, return_dict):
    status, monthly_data = get_monthly_data(terms_and_tickers)
    print(monthly_data)
    if not status:
        return False, "Error getting monthly data"

    for data in monthly_data:
        return_dict[data[0]] = data

    return True, monthly_data


def main():
    if not create_vanga_me_db_file():
        print('DB CONNECTION ERROR')

    monthly_start_counter = perf_counter()
    get_future_prediction_counter = perf_counter()

    proc = None
    manager = mlpcs.Manager()

    while True:
        if (perf_counter() - monthly_start_counter) > 60 * 60:  # once every hour
            monthly_dict = manager.dict()
            month_proc = mlpcs.Process(target=get_data_for_monthly_accuracy_table_view,
                                       args=tuple([global_term_and_tickers, monthly_dict]))

            month_proc.name = "monthly"
            month_proc.start()
            month_proc.join()

            monthly_start_counter = perf_counter()

        if (perf_counter() - get_future_prediction_counter) > 60 * 5:  # once every 5 minutes
            future_dict = manager.dict()

            future_proc = mlpcs.Process(target=get_future_predictions,
                                        args=tuple([global_term_and_tickers, future_dict]))

            future_proc.name = "future"
            future_proc.start()
            future_proc.join()

            get_future_prediction_counter = perf_counter()


if __name__ == '__main__':
    # running main
    main()
