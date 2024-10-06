<!-- SPDX-License-Identifier: zlib-acknowledgement -->
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
   TODO: this is for classification? so might differ for regression
3. Initialise architecture chosen:
```
model = models.resnet18(pretrained=True)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 2)
```
   resnet trained on imagenet
   a fully connected layer is typically final layer, so 1000 neurons for 1000 output classes?
   to modify it, create new fc layer with same input features, but 2 outputs 
4. Define loss, optimiser and hyperparameters
crossentropy loss common for classification
adam is common optimiser with fast convergence rate
```
loss_func = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
num_epochs = 10
```
5. Train through epochs
```
model.train()

optimiser.zero_grad()

forward pass?
outputs = model(inputs) # run image through all layers, e.g. convolution, pooling, activation etc.
loss = loss_func(outputs, labels)

backward pass?
loss.backward() # update model parameters based on loss
optimiser.step()
```

6. Validate model on test set
```
model.eval()
loss_func()
```
Go back to step 4 and before and make adjustments to improve

7. Save model
```
torch.save(model.state_dict(), 'apple_model.pth')
```



## Graphs
x-axis epochs
- Loss is how far predictions from true labels.
  Measures correctness and confidence.
  Based on loss function, e.g. for classification might use binary cross-entropy
- Accuracy is proportion of correct predictions. 

spikes in validation indicate overfitting
