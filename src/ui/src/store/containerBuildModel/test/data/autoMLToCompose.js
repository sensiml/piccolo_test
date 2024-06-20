/*
Copyright 2017-2024 SensiML Corporation

This file is part of SensiML™ Piccolo AI™.

SensiML Piccolo AI is free software: you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License
as published by the Free Software Foundation, either version 3 of
the License, or (at your option) any later version.

SensiML Piccolo AI is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with SensiML Piccolo AI. If not, see <https://www.gnu.org/licenses/>.
*/

export default [
  {
    name: "Pipeline Settings",
    customName: "Pipeline Settings",
    nextSteps: null,
    mandatory: true,
    type: "AUTOML_PARAMS",
    subtype: [],
    transformList: [],
    excludeTransform: [],
    data: {
      disable_automl: false,
      "prediction_target(%)": {
        f1_score: 100,
      },
      hardware_target: {
        classifiers_sram: 32000,
      },
      selectorset: true,
      set_selectorset: [
        "Information Gain",
        "t-Test Feature Selector",
        "Univariate Selection",
        "Tree-based Selection",
      ],
      tvo: true,
      set_training_algorithm: [
        "Hierarchical Clustering with Neuron Optimization",
        "RBF with Neuron Allocation Optimization",
        "Random Forest",
        "xGBoost",
        "Train Fully Connected Neural Network",
      ],
      iterations:2,
      population_size: 40,
      allow_unknown: false,
    },
    limit: 1,
    set: false,
    id: "a34ec83f-48c8-44d3-9f27-174e35ceba5b",
    index: 0,
  },
  {
    name: "Input Query",
    customName: "Q1",
    nextSteps: [
      "Sensor Transform",
      "Sensor Filter",
      "Segmenter",
      "Sampling Filter",
      "Augmentation",
    ],
    mandatory: true,
    type: "Query",
    subtype: ["Query"],
    transformFilter: [
      {
        Type: "Query",
        Subtype: "Query",
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: 1,
    set: false,
    id: "744e9b21-1c1f-4d56-adfa-9448eca72808",
    data: {
      name: "Q1",
      use_session_preprocessor: false,
    },
    options: {
      descriptionParameters: {
        name: "Q1",
        label_column: "Label",
        columns: ["channel_0"],
        metadata_columns: ["segment_uuid", "Set"],
        session: "Training Session",
        cacheStatus: "CACHED",
      },
    },
  },
  {
    name: "Augmentation",
    customName: "Random Crop",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "c4ee5a69-ea51-4205-b7ce-06fc8512ef32",
    data: [
      {
        name: "Random Crop",
        params: {
          filter: {
            Set: ["Train"],
          },
          crop_size: 16000,
          target_labels: ["No", "Off", "On", "Yes"],
          overlap_factor: 1,
          selected_segments_size_limit: [16001, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Augmentation",
    customName: "Random Crop",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "44efb7b3-cb73-4485-be6e-4a366a668df7",
    data: [
      {
        name: "Random Crop",
        params: {
          filter: {
            Set: ["Train"],
          },
          crop_size: 16000,
          target_labels: ["Unknown"],
          overlap_factor: 1.5,
          selected_segments_size_limit: [1, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Augmentation",
    customName: "Time Shift",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "2d1e1138-18e6-4103-9064-9f12835aeb50",
    data: [
      {
        name: "Time Shift",
        params: {
          filter: {
            Set: ["Train"],
          },
          replace: false,
          fraction: 1,
          shift_range: [-1000, 1000],
          target_labels: ["No", "Off", "On", "Yes"],
          averaging_window_size: 100,
          selected_segments_size_limit: [1, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Augmentation",
    customName: "Time Stretch, Pitch Shift",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "bfb26864-8ac9-4e75-aabe-967bd39a153c",
    data: [
      {
        name: "Time Stretch",
        params: {
          filter: {
            Set: ["Train"],
          },
          replace: false,
          fraction: 1,
          target_labels: ["No", "Off", "On", "Yes"],
          stretch_factor_range: [0.95, 1.05],
          selected_segments_size_limit: [1, 100000],
        },
      },
      {
        name: "Pitch Shift",
        params: {
          filter: {
            Set: ["Train"],
          },
          replace: false,
          fraction: 1,
          sample_rate: 16000,
          shift_range: [-8, 8],
          input_columns: [],
          target_labels: ["No", "Off", "On", "Yes"],
          step_per_octave: 256,
          selected_segments_size_limit: [1, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Augmentation",
    customName: "Scale Amplitude",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "a68de2cf-0cdb-40ad-afaa-3aaf8c54c9a0",
    data: [
      {
        name: "Scale Amplitude",
        params: {
          filter: {
            Set: ["Train"],
          },
          replace: true,
          fraction: 3,
          scale_range: [0.5, 3],
          input_columns: [],
          target_labels: ["No", "Off", "On", "Yes"],
          selected_segments_size_limit: [1, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Augmentation",
    customName: "Add Noise",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Augmentation",
    subtype: [],
    transformFilter: [
      {
        Type: "Augmentation",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "9cf9caea-60e1-4b1a-9051-ad4ca48da65d",
    data: [
      {
        name: "Add Noise",
        params: {
          filter: {
            Set: ["Train"],
          },
          replace: true,
          fraction: 5,
          noise_types: ["pink", "white"],
          input_columns: [],
          target_labels: ["No", "Off", "On", "Yes"],
          background_scale_range: [50, 400],
          selected_segments_size_limit: [1, 100000],
        },
      },
    ],
    options: {},
  },
  {
    name: "Segmenter",
    customName: "Windowing",
    nextSteps: [
      "Segment Transform",
      "Segment Filter",
      "Augmentation",
      "Sampling Filter",
      "Feature Generator",
    ],
    mandatory: true,
    type: "Segmenter",
    subtype: [],
    transformFilter: [
      {
        Type: "Segmenter",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: 1,
    set: false,
    id: "f2b778e6-17cb-4c41-8484-a5c04cee0e62",
    data: {
      delta: 320,
      input_data: "temp.augmentation_set5",
      train_delta: 0,
      window_size: 480,
      group_columns: ["Label", "Set", "segment_uuid"],
      return_segment_index: false,
      transform: "Windowing",
    },
    options: {},
  },
  {
    name: "Segment Filter",
    customName: "Segment Energy Threshold Filter",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Transform",
    subtype: ["Segment Filter"],
    transformFilter: [
      {
        Type: "Transform",
        Subtype: "Segment Filter",
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: null,
    set: false,
    id: "dec6fbf8-f4ba-4341-89c1-5161c1d072e3",
    data: {
      delay: 35,
      backoff: 0,
      threshold: 1000,
      input_data: "temp.Windowing0",
      input_column: "channel_0",
      disable_train: true,
      group_columns: ["Label", "SegmentID", "Set", "segment_uuid"],
      transform: "Segment Energy Threshold Filter",
    },
    options: {},
  },
  {
    name: "Feature Generator",
    customName: "Feature Generator",
    nextSteps: [
      "Data Balancing",
      "Feature Selector",
      "Feature Transform",
      "Outlier Filter",
      "Feature Quantization",
    ],
    mandatory: true,
    type: "Feature Generator",
    subtype: [],
    transformFilter: [
      {
        Type: "Feature Generator",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [],
    limit: 1,
    set: true,
    id: "22c6c9f6-07bc-4585-a6cc-a0bf98641ca4",
    data: [
      {
        name: "MFCC",
        params: {
          columns: ["channel_0"],
          sample_rate: 16000,
          cepstra_count: 23,
        },
      },
    ],
    options: {},
  },
  {
    name: "Feature Quantization",
    customName: "Min Max Scale",
    nextSteps: [
      "Data Balancing",
      "Feature Selector",
      "Feature Transform",
      "Outlier Filter",
      "Training Algorithm",
      "Feature Grouping",
    ],
    mandatory: true,
    type: "",
    subtype: [],
    transformFilter: [],
    transformList: ["Min Max Scale"],
    excludeTransform: [],
    limit: 1,
    set: false,
    id: "3608edb8-604a-4f22-8132-deb64463e941",
    data: {
      pad: 0,
      max_bound: 255,
      min_bound: 0,
      input_data: "temp.generator_set0",
      passthrough_columns: ["Label", "SegmentID", "Set", "segment_uuid"],
      feature_min_max_defaults: [200000, -200000],
      feature_min_max_parameters: {},
      transform: "Min Max Scale",
    },
    options: {},
  },
  {
    name: "Feature Transform",
    customName: "Feature Cascade",
    nextSteps: [
      "Data Balancing",
      "Feature Selector",
      "Feature Transform",
      "Outlier Filter",
      "Feature Grouping",
    ],
    mandatory: false,
    type: "Transform",
    subtype: ["Feature Vector"],
    transformFilter: [
      {
        Type: "Transform",
        Subtype: "Feature Vector",
      },
    ],
    transformList: [],
    excludeTransform: ["Min Max Scale"],
    limit: null,
    set: false,
    id: "dec60f7f-d9b1-4b83-afdf-b6f2a98b6774",
    data: {
      slide: false,
      input_data: "temp.Min_Max_Scale0",
      num_cascades: 49,
      group_columns: ["Label", "SegmentID", "Set", "segment_uuid"],
      training_delta: 49,
      training_slide: true,
      transform: "Feature Cascade",
    },
    options: {},
  },
  {
    name: "Feature Selector",
    customName: "Feature Selector",
    nextSteps: ["Parent"],
    mandatory: false,
    type: "Feature Selector",
    subtype: [],
    transformFilter: [
      {
        Type: "Feature Selector",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: ["Custom Feature Selection", "Custom Feature Selection By Index"],
    limit: 1,
    set: true,
    id: "8d4b712d-aa09-4293-aa84-8a6b809a5dc3",
    data: [
      {
        name: "Information Gain",
        params: {
          feature_number: 2,
        },
      },
    ],
    options: {},
  },
  {
    name: "Classifier",
    customName: "TensorFlow Lite for Microcontrollers",
    nextSteps: ["Training Algorithm"],
    mandatory: true,
    type: "Classifier",
    subtype: [],
    transformFilter: [
      {
        Type: "Classifier",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: ["TF Micro"],
    limit: 1,
    set: false,
    id: "61bcf190-3d2a-4f0a-8181-cc0fa6f71dca",
    data: {
      transform: "TensorFlow Lite for Microcontrollers",
    },
    options: {},
  },
  {
    name: "Training Algorithm",
    customName: "Transfer Learning",
    nextSteps: ["Validation"],
    mandatory: true,
    type: "Training Algorithm",
    subtype: [],
    transformFilter: [
      {
        Type: "Training Algorithm",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: [
      "Load Model PME",
      "Load Model TF Micro",
      "Load Model TensorFlow Lite for Microcontrollers",
      "Load Neuron Array",
    ],
    limit: 1,
    set: false,
    id: "d58f2211-d3f5-4f29-bbbf-e9ac4527aa63",
    data: {
      epochs: 25,
      metrics: "accuracy",
      drop_out: 0.1,
      threshold: 0.6,
      base_model: "06364704-6a2e-11ed-a1eb-0242ac120002",
      batch_size: 32,
      input_type: "int8",
      dense_layers: [],
      learning_rate: 0.001,
      loss_function: "categorical_crossentropy",
      estimator_type: "classification",
      final_activation: "softmax",
      random_time_mask: true,
      random_bias_noise: true,
      batch_normalization: true,
      random_sparse_noise: true,
      training_size_limit: 1000,
      tensorflow_optimizer: "adam",
      random_frequency_mask: true,
      validation_size_limit: 500,
      auxiliary_augmentation: true,
      early_stopping_patience: 2,
      early_stopping_threshold: 0.9,
      transform: "Transfer Learning",
    },
    options: {},
  },
  {
    name: "Validation",
    customName: "Split by Metadata Value",
    nextSteps: [],
    mandatory: true,
    type: "Validation Method",
    subtype: [],
    transformFilter: [
      {
        Type: "Validation Method",
        Subtype: null,
      },
    ],
    transformList: [],
    excludeTransform: ["Leave-One-Subject-Out", "Set Sample Validation"],
    limit: 1,
    set: false,
    id: "c445a838-281a-4c55-a21d-b6d2050dbc43",
    data: {
      metadata_name: "Set",
      training_values: ["Train"],
      validation_values: ["Validate"],
      transform: "Split by Metadata Value",
    },
    options: {},
  },
];