import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def scale_data255(data, keys):
    """Scales the values of data in each column to a range of [0,255]
    # param data - pandas.DataFrame where columns are data and class labels
    # param keys - list of str with keys for the feature columns from the DataFrame
    """
    data255 = data.copy()
    for k in keys:
        maxVal = data[k].max()  # find the maximum value in the feature data
        minVal = data[k].min()  # find the minimum
        scale = 255 / (maxVal - minVal)  # calculate the scaling factor
        shift = minVal * scale  # calculate the zero shift
        data255[k] = data[k] * scale - shift
    return data255[keys].astype(int)  # convert to integer for return


def identical_model_check(all_models, new_model):
    """Tests if new_model is present in the all_models Dataframe"""
    all_models_list = all_models.tolist()
    new_model = np.array(
        (pd.DataFrame(new_model)[["AIF", "Category", "Vector"]])
    ).tolist()
    bool_model_list = []
    for i in all_models_list:  # all_models:
        temp = np.array(pd.DataFrame(i)[["AIF", "Category", "Vector"]]).tolist()
        # is this model not unique?
        bool_vector_list = []
        for j in new_model:
            if j in temp:
                bool_vector_list.append(True)
            else:
                bool_vector_list.append(False)

        if all(bool_vector_list):
            # if new model is found in the df
            bool_model_list.append(True)
            break
        else:
            bool_model_list.append(False)

    if any(bool_model_list):
        # this model already in the df
        # print 'index end of the function: ', bool_model_list.index(True)
        return False, bool_model_list.index(True)
    else:
        # this model is new
        return True, 0


def add_result_to_dataframe(result, df=[]):
    """Utility function for saving results in a pandas DataFrame.
    The initial empty DataFrame is constructed if no DataFrame is provided
    # param result - dict from  output of KBDataScienceKit.create_modelgenerator()
    # param df - pandas.DataFrame generated by this function
    """
    if (
        isinstance(df, pd.DataFrame) == False
    ):  # Instantiates new DataFrame unless one is provided to add new result
        columns = [
            "ProperClassificationPercent",
            "NeuronsUsed",
            "Parameters",
            "neurons",
            "train_set",
            "ConfusionMatrix",
        ]  # 'norm', 'turbo', 'min_aif', 'max_aif',
        df = pd.DataFrame([], columns=columns)  # Initialize DataFrame on first loop

    num_iterations = len(result["models"].keys())
    for i in range(num_iterations):
        results_param_list = []
        model_name = result["models"].keys()[i]
        parameters_list = [
            result["config"]["distance_mode"],
            result["config"]["turbo"],
            result["config"]["min_aif"],
            result["config"]["max_aif"],
        ]
        unique_model = True
        model_index = 0

        # if any model has the same NeuronsUsed with new model, it checks the df to find identical_model
        if any(df["NeuronsUsed"] == len(result["models"][model_name]["neurons"])):
            # all data that have the same #neurons with new model
            # True : it is a new model, False: it is already in df
            temp_df = df[
                df["NeuronsUsed"] == len(result["models"][model_name]["neurons"])
            ]  # ['neurons']
            unique_model, model_index = identical_model_check(
                temp_df["neurons"], result["models"][model_name]["neurons"]
            )
            # if not unique_model: print model_index, '--->', temp_df['NeuronsUsed'].index[model_index]
            model_index = temp_df["NeuronsUsed"].index[model_index]

        if unique_model:
            parameters_df = pd.DataFrame(
                columns=["norm", "turbo", "min_aif", "max_aif"]
            )
            parameters_df.loc[0] = parameters_list

            results_param_list.append(
                int(
                    result["models"][model_name]["metrics"]["validation"][
                        "ProperClassificationPercent"
                    ]
                )
            )
            results_param_list.append(
                result["models"][model_name]["metrics"]["validation"]["NeuronsUsed"]
            )
            results_param_list.append(parameters_df)
            results_param_list.append(
                result["models"][model_name]["neurons"]
            )  # add neurons to the DataFrame
            results_param_list.append(
                result["models"][model_name]["train_set"]
            )  # add order of training data to the DataFrame
            results_param_list.append(
                result["models"][model_name]["metrics"]["validation"]["ConfusionMatrix"]
            )  # add confusion matrix

            df.loc[len(df)] = results_param_list
        else:
            list_size = len(df["Parameters"][model_index])
            df["Parameters"][model_index].loc[list_size + 1] = parameters_list
    return df


def sort_accuracy_neurons(results_params, param_name="", param_values=[]):
    """Sorts model_generator execution results by descending ProperClassificationPercent and ascending NeuronsUsed
    If parameter name and values are provided, the models are divided into the parameter values (eg. param_name='norm', param_values=['L1','Lsup'])
    # results_params - pandas.DataFrame,  model_generator execution results in a DataFrame created by add_result_to_dataframe()
    # param_name - str, name of parameter to be seperated
    # param_values - list, values for the parameter groups to be compared
    """
    if param_name == "":
        return results_params.sort_values(
            ["ProperClassificationPercent", "NeuronsUsed"], ascending=[False, True]
        )
    sorted_results_params = {}
    for pv in param_values:
        p = str(pv)
        pv_list = []
        for i in range(len(results_params)):
            pv_list.append(pv in results_params["Parameters"][i][param_name].tolist())
        results_params_pv = results_params[pv_list]
        print p + " models = ", len(results_params_pv)
        sorted_results_params[p] = results_params_pv.sort_values(
            ["ProperClassificationPercent", "NeuronsUsed"], ascending=[False, True]
        )
    return sorted_results_params


def parsing_df(df):
    min_aif_list = []
    max_aif_list = []
    ProperClassificationPercent_list = []
    for i in df.index:
        for j in df["Parameters"][i].index:
            min_aif_list.append(df["Parameters"][i]["min_aif"][j])
            max_aif_list.append(df["Parameters"][i]["max_aif"][j])
            ProperClassificationPercent_list.append(
                df["ProperClassificationPercent"][i]
            )
    return min_aif_list, max_aif_list, ProperClassificationPercent_list


def plot_compare2_accuracy_neurons(sorted_results, param_name):
    """Plots 2 groups of results
    # sorted_results - pandas.DataFrame,   results sorted by sort_accuracy_neurons()
    # param_name - str, name of parameter being compared
    """
    keys = sorted_results.keys()
    fig, ax1 = plt.subplots(figsize=(8, 6))
    plt.title(
        "Accuracy and neurons used for "
        + param_name
        + " "
        + keys[0]
        + " and "
        + keys[1],
        fontsize=14,
        fontweight="bold",
    )
    ax1.plot(
        sorted_results[keys[0]]["ProperClassificationPercent"],
        color="b",
        label=keys[0] + " Accuracy",
        linewidth=1,
    )
    ax1.plot(
        sorted_results[keys[1]]["ProperClassificationPercent"],
        color="r",
        label=keys[1] + " Accuracy",
    )
    ax1.set_ylabel("Accuracy", fontsize=14)
    ax1.set_xlabel("Model number, sorted by accuracy", fontsize=14)
    ax1.set_ylim(0, 100)
    ax1.tick_params(axis="both", which="major", labelsize=14)
    ax1.legend(loc="upper right")
    ax2 = ax1.twinx()
    ax2.plot(
        sorted_results[keys[0]]["NeuronsUsed"],
        "--",
        color="b",
        label=keys[0] + " #Neurons",
        linewidth=1,
    )
    ax2.plot(
        sorted_results[keys[1]]["NeuronsUsed"],
        "--",
        color="r",
        label=keys[1] + " #Neurons",
    )
    ax2.set_ylabel("Number of neurons", color="k", fontsize=14)
    ax2.set_ylim(0, 100)
    ax2.tick_params(axis="both", which="major", labelsize=14)
    plt.xlim(0, 500)
    plt.xlim(0, max(len(sorted_results[keys[0]]), len(sorted_results[keys[1]])))
    plt.legend(loc="lower left")


def plot_3d_accuracy_min_max_aif(results_params):
    """Creates a 3d plot of the accuracy as a function of minimum and maximum AIF
    # results_params - pandas.DataFrame,  model_generator execution results in a DataFrame created by add_result_to_dataframe()
    """
    sorted_results_norm = sort_accuracy_neurons(results_params, "norm", ["L1", "Lsup"])
    results_params_L1 = sorted_results_norm["L1"]
    results_params_Lsup = sorted_results_norm["Lsup"]
    min_aif_list_L1, max_aif_list_L1, ProperClassificationPercent_list_L1 = parsing_df(
        results_params_L1
    )
    (
        min_aif_list_Lsup,
        max_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
    ) = parsing_df(results_params_Lsup)

    # 3D plot of accuracy vs max_aif vs min_aif
    fig = plt.figure(figsize=(16, 6))
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.scatter(
        min_aif_list_L1,
        max_aif_list_L1,
        ProperClassificationPercent_list_L1,
        c="b",
        label="L1",
    )
    ax.text2D(
        0.5,
        0.95,
        "Accuracy versus AIF parameters for L1 and Lsup norms",
        transform=ax.transAxes,
        fontsize=14,
        fontweight="bold",
    )
    ax.tick_params(axis="both", which="major", labelsize=14)
    ax.set_xlabel("min_aif", fontsize=14)
    ax.set_xlim(min(min_aif_list_L1), max(min_aif_list_L1))
    ax.set_ylabel("max_aif", fontsize=14)
    ax.set_ylim(min(max_aif_list_L1), max(max_aif_list_L1))
    ax.set_zlabel("Accuracy", fontsize=14)
    ax.set_zlim(0, 100)
    ax.legend(bbox_to_anchor=(0.75, 0.92), loc=2)
    ax2 = fig.add_subplot(1, 2, 2, projection="3d")
    ax2.scatter(
        min_aif_list_Lsup,
        max_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
        c="r",
        marker="^",
        label="Lsup",
    )
    ax2.tick_params(axis="both", which="major", labelsize=14)
    ax2.set_xlabel("min_aif", fontsize=14)
    ax2.set_xlim(min(min_aif_list_Lsup), max(min_aif_list_Lsup))
    ax2.set_ylabel("max_aif", fontsize=14)
    ax2.set_ylim(min(max_aif_list_Lsup), max(max_aif_list_Lsup))
    ax2.set_zlabel("Accuracy", fontsize=14)
    ax2.set_zlim(0, 100)
    ax2.legend(bbox_to_anchor=(0.7, 0.92), loc=2, numpoints=1)


def plot_2d_accuracy_min_max_aif(results_params):
    """Creates a 2d projection plot of the accuracy as a function of minimum and maximum AIF
    # results_params - pandas.DataFrame,  model_generator execution results in a DataFrame created by add_result_to_dataframe()
    """
    sorted_results_norm = sort_accuracy_neurons(results_params, "norm", ["L1", "Lsup"])
    results_params_L1 = sorted_results_norm["L1"]
    results_params_Lsup = sorted_results_norm["Lsup"]
    min_aif_list_L1, max_aif_list_L1, ProperClassificationPercent_list_L1 = parsing_df(
        results_params_L1
    )
    (
        min_aif_list_Lsup,
        max_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
    ) = parsing_df(results_params_Lsup)

    # Projection onto min_aif
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 4), sharey=True)
    plt.suptitle(
        "Accuracy vs minimum AIF for L1 and Lsup norms", fontsize=14, fontweight="bold"
    )
    ax1.plot(
        min_aif_list_L1,
        ProperClassificationPercent_list_L1,
        "o",
        label="L1",
        color="b",
        alpha=0.6,
    )
    ax1.tick_params(axis="both", which="major", labelsize=14)
    ax1.set_ylabel("Accuracy", fontsize=14)
    ax1.legend(loc="lower right", numpoints=1, fontsize=14)
    ax1.set_xlabel("min_aif", fontsize=14)
    ax2.plot(
        min_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
        "o",
        label="Lsup",
        color="r",
        alpha=0.6,
    )
    ax2.tick_params(axis="both", which="major", labelsize=14)
    ax2.legend(loc="lower right", numpoints=1, fontsize=14)
    ax2.set_xlabel("min_aif", fontsize=14)

    # Projection onto max_aif
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 4), sharey=True)
    plt.suptitle(
        "Accuracy vs maximum AIF for L1 and Lsup norms", fontsize=14, fontweight="bold"
    )
    ax1.plot(
        max_aif_list_L1,
        ProperClassificationPercent_list_L1,
        "o",
        label="L1",
        color="b",
        alpha=0.6,
    )
    ax1.tick_params(axis="both", which="major", labelsize=14)
    ax1.set_ylabel("Accuracy", fontsize=14)
    ax1.legend(loc="lower right", numpoints=1, fontsize=14)
    ax1.set_xlabel("max_aif", fontsize=14)
    ax2.plot(
        max_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
        "o",
        label="Lsup",
        color="r",
        alpha=0.6,
    )
    ax2.tick_params(axis="both", which="major", labelsize=14)
    ax2.legend(loc="lower right", numpoints=1, fontsize=14)
    ax2.set_xlabel("max_aif", fontsize=14)


def plot_accuracy_ratio_max_min_aif(
    results_params,
    max_min_aif_L1=16384,
    min_max_aif_L1=0,
    max_min_aif_Lsup=255,
    min_max_aif_Lsup=0,
):
    """Creates a 2d projection plot of the accuracy as a function of minimum and maximum AIF
    # results_params - pandas.DataFrame,  model_generator execution results in a DataFrame created by add_result_to_dataframe()
    # max_min_aif_L1 - int, largest minimum AIF parameter to be included in plot for L1 norm models
    # min_max_aif_L1 - int, smallest maximum AIF parameter to be included in plot for L1 norm models
    # max_min_aif_Lsup - int, largest minimum AIF parameter to be included in plot for Lsup norm models
    # min_max_aif_Lsup - int, smallest maximum AIF parameter to be included in plot for Lsup norm models
    """
    sorted_results_norm = sort_accuracy_neurons(results_params, "norm", ["L1", "Lsup"])
    results_params_L1 = sorted_results_norm["L1"]
    results_params_Lsup = sorted_results_norm["Lsup"]
    min_aif_list_L1, max_aif_list_L1, ProperClassificationPercent_list_L1 = parsing_df(
        results_params_L1
    )
    ratio_max_min_aif_L1 = np.array(max_aif_list_L1) / np.array(min_aif_list_L1)
    param_accuracy_L1 = pd.DataFrame(
        {
            "ProperClassificationPercent": ProperClassificationPercent_list_L1,
            "min_aif": min_aif_list_L1,
            "max_aif": max_aif_list_L1,
            "ratio_max_min": ratio_max_min_aif_L1,
        }
    )
    (
        min_aif_list_Lsup,
        max_aif_list_Lsup,
        ProperClassificationPercent_list_Lsup,
    ) = parsing_df(results_params_Lsup)
    ratio_max_min_aif_Lsup = np.array(max_aif_list_Lsup) / np.array(min_aif_list_Lsup)
    param_accuracy_Lsup = pd.DataFrame(
        {
            "ProperClassificationPercent": ProperClassificationPercent_list_Lsup,
            "min_aif": min_aif_list_Lsup,
            "max_aif": max_aif_list_Lsup,
            "ratio_max_min": ratio_max_min_aif_Lsup,
        }
    )
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 4), sharey=True)
    plt.suptitle(
        "Accuracy vs Ratio of min to max AIF for L1 and Lsup norms",
        fontsize=14,
        fontweight="bold",
    )
    ax1.plot(
        param_accuracy_L1["ratio_max_min"][
            (param_accuracy_L1["min_aif"] < max_min_aif_L1)
            & (param_accuracy_L1["max_aif"] > min_max_aif_L1)
        ],
        param_accuracy_L1["ProperClassificationPercent"][
            (param_accuracy_L1["min_aif"] < max_min_aif_L1)
            & (param_accuracy_L1["max_aif"] > min_max_aif_L1)
        ],
        ".",
        label="L1",
        color="b",
        alpha=0.6,
    )
    ax1.tick_params(axis="both", which="major", labelsize=14)
    ax1.set_ylabel("Accuracy", fontsize=14)
    ax1.legend(loc="lower right", numpoints=1, fontsize=14)
    ax1.set_xlabel("max_aif/min_aif", fontsize=14)
    ax1.set_ylim(0, 100)
    ax2.plot(
        param_accuracy_Lsup["ratio_max_min"][
            (param_accuracy_Lsup["min_aif"] < max_min_aif_Lsup)
            & (param_accuracy_Lsup["max_aif"] > min_max_aif_Lsup)
        ],
        param_accuracy_Lsup["ProperClassificationPercent"][
            (param_accuracy_Lsup["min_aif"] < max_min_aif_Lsup)
            & (param_accuracy_Lsup["max_aif"] > min_max_aif_Lsup)
        ],
        ".",
        label="Lsup",
        color="r",
        alpha=0.6,
    )
    ax2.tick_params(axis="both", which="major", labelsize=14)
    ax2.legend(loc="lower right", numpoints=1, fontsize=14)
    ax2.set_xlabel("max_aif/min_aif", fontsize=14)