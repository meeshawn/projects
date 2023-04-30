## Vision Transformer based Image Classification

1. Developed an image classifier for handwritten MNIST digits by utilizing the framework of an Encoder model from Transformers to convert images into a sequence of sub-images and
discover latent semantics between them which is further used to train an MLP to classify digits between [0-9].

2. Model selection was performed using 3-fold cross validation across the following set of hyperparameters:
  - Number of Encoder Blocks $\in [2,3]$
  - Number of Hidden Units in the 2nd layer of the MLP $\in [16,32]$

3. Results of model selection and the training results of the best model are provided in the .ipynb file.
