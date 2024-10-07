<!-- SPDX-License-Identifier: zlib-acknowledgement -->
TODO: how are labels presented in alicia code?

## Graphs
x-axis epochs
- Loss is how far predictions from true labels.
  Measures correctness and confidence.
  Based on loss function, e.g. for classification might use binary cross-entropy
- Accuracy is proportion of correct predictions. 

spikes in validation indicate overfitting

## Process
1. Load labelled data into training and validation:
   ```
   data = ImageFolder(root='data/fruits', transform=custom_data_transforms_struct)
   train, validation = random_split(data, [.8, .2])
   ```
   examples of preprocessing: resizing, augmentation, normalisation etc.
2. Create data loader to feed batches of data to model:
   ```
   train_loader = DataLoader(train, batch_size=32, shuffle=True, num_workers=4)
   ```
3. Initialise architecture chosen:
   A fully connected (fc) layer has all previous layers connected to outputs.
   It's typically a final layer.
   So, the number of outputs is number of classes.
   Resnet trained on Imagenet, so 1000 output classes.
   For binary classication, just want 2 outputs.
```
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
```
   For small datasets, overfitting can be an issue.
   Have various regularisation techniques to overcome.
   Dropout will randomly remove neurons, so don't rely on them.
   Slower convergence time, higher accuracy
```
model.fc = nn.Sequential(
    nn.Dropout(0.5),
    nn.Linear(num_ftrs, 2)
)
```
4. Define loss, optimiser and hyperparameters
```
    Crossentropy loss common for classification.
    ADAM is common optimiser with fast convergence rate.
```
loss_func = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
num_epochs = 10
```
    However, if overfitting, would want lower learning rate that is dynamically adjusted.
```
optimizer = optim.Adam(model.parameters(), lr=0.0001)
scheduler = ReduceLROnPlateau(optimizer, mode='min', factor=0.1, patience=3)
```

5. Train through epoch
   Involves forward pass running images through all layers, e.g. convolution, pooling, activation etc.
   Then backward pass, updating model parameters based on loss
```
model.train()

optimiser.zero_grad()

outputs = model(inputs) 
loss = loss_func(outputs, labels)

loss.backward() 
optimiser.step()
```

6. Validate model on test set
```
model.eval()
loss_func()
```
  To prevent overfitting, can do early stopping regularisation.
  Specifically, stop training if validation loss doesn't improve for a number of epochs.

Go back to step 4 and before and make adjustments to improve
7. Save model
```
torch.save(model.state_dict(), 'apple_model.pth')
```
