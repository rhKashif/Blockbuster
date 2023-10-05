# Blockbuster Video Rental System

Welcome to the Blockbuster Video Rental System README! This project is an object-oriented implementation of a rental system for Blockbuster video, inspired by the 90s era. It allows for the management of videos, customers, rentals, and even introduces features like late return fines and the inclusion of DVDs and vending machines.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
3. [Key Features](#key-features)
4. [Classes and Objects](#classes-and-objects)
5. [Usage](#usage)
6. [Contributing](#contributing)
7. [License](#license)

## Project Overview

In this project, we've created a rental system for Blockbuster video, based on the following specifications:

- Videos have attributes like title, year of release, runtime, and rental price.
- Blockbuster stores stock multiple videos for rental.
- Stores can look up videos by name.
- Customers can rent up to 3 videos at a time, with the requirement to rewind before returning.
- Late returns incur fines.
- Customers with significant outstanding fines can't rent videos until their fines are paid off.
- In the final challenge, new types of media (DVDs) for Blockbuster are introduced, along with Blockbuster vending machines.

## Getting Started

To get started with this project, make sure you have Python installed on your system. You can clone this repository to your local machine:

```bash
git clone https://github.com/rhkashif/Blockbuster.git
```

## Usage

The provided script `blockbuster.py` demonstrates how to use the Blockbuster Video Rental System. It creates customers, videos, and stores, rents a video to a customer, and returns it. You can modify and expand on this script to suit your needs.

## Testing

We have a comprehensive test suite to ensure the functionality and reliability of the Blockbuster Video Rental System. We use [pytest](https://pytest.org/) as our testing framework.

To run the tests locally, follow these steps:

1. Make sure you have Python and pytest installed on your system.
2. Open your terminal or command prompt.
3. Navigate to the project's root directory.
4. Run the following command:

```bash
pytest test_blockbuster_challenge.py
pytest test_blockbuster_trainee.py
```

## Contributing

We welcome contributions to this project. Feel free to open issues, suggest improvements, or submit pull requests. Please follow best practices and contribute in a constructive manner.


