
# Dodge-The-Blocks-NEAT-AI

## About ##

NEAT (NeuroEvolution of Augmenting Topologies) is a method developed by Kenneth O. Stanley for evolving arbitrary neural
networks inspired from real-world eevolution.

For further information regarding general concepts and theory, please see
[Selected Publications](http://www.cs.ucf.edu/~kstanley/#publications)

-----

This project is an implementation of NEAT to evolve an AI that plays a 2D Game (Dodge the Blocks) that mimicks simple obstacle avoidance and range perception to extraordinary levels

### Game Mechanics
The game environment is a simple 2D world where obstacles spawn and fall at intervals. The controls are binary (left or right)

The AI uses a Recurrent Neural Network with;

- An input layer : The coordinates of the falling blocks
- An hidden layer
- An output layer : To dictate one of two actions ( move left or move right ) 


Run the code on Gitpod and play against the AI 
[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/Timmyy3000/Dodge-The-Blocks-NEAT-AI)


## Tools

The web app was built in Python using the following libraries:
* pygame
* neat
* numpy

