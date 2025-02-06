# Aiza - AI Personal Assistant

![Aiza Logo](https://github.com/WasifKhan/Aiza/blob/master/Aiza%20logo.png)

## Overview
Aiza is an advanced AI personal assistant designed to learn and adapt to your preferences using information from sources you provide access to. By integrating with Google and Meta services, Aiza helps streamline your digital life, offering personalized assistance based on your data.

## Features
- **Personalized AI**: Learns from your interactions to provide tailored responses.
- **Seamless Integration**: Supports data access from Google Drive, Gmail, Meta services, and more.
- **Modular Architecture**: Easily extend functionality with plugins and APIs.
- **Secure & Privacy-Focused**: Data security and user control are top priorities.

## Repository Structure
```
Aiza/
├── src/                    # Source code
│   ├── main.py             # Entry point of the application
│   ├── aiza.py             # Core AI logic
│   ├── data_loader/        # Data ingestion modules
│   ├── models/             # AI/ML models for personalization
│   ├── artifacts/          # Stored outputs
│
├── test/                   # Unit and integration tests
│
├── README.md               # Project documentation
├── requirements.txt        # Python dependencies
├── LICENSE                 # License file
```

## Installation
### Prerequisites
Ensure you have Python 3 installed.

```sh
sudo apt update && sudo apt install python3 python3-pip -y
```

Clone the repository and install dependencies:
```sh
git clone https://github.com/wasifkhan/aiza.git
cd aiza
pip install -r requirements.txt
```

## Usage
To start Aiza, run:
```sh
python src/main.py generate_data
python src/main.py learn_user
python src/main.py run
```
You may be prompted to authenticate and provide permissions to access Google and Meta services.

## Configuration
Aiza requires API credentials for Google and Meta services. Set up your environment variables:
```sh
export GOOGLE_API_KEY="your_google_api_key"
export META_ACCESS_TOKEN="your_meta_access_token"
```

## Testing
Run unit tests to ensure everything is working correctly:
```sh
pytest test/
```

## Contributing
Contributions are welcome! Follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-xyz`)
3. Commit your changes (`git commit -m "Added feature xyz"`)
4. Push to the branch (`git push origin feature-xyz`)
5. Open a pull request

## Contact
**Author:** Wasif Khan  
📧 Email: [wasif.k1112@gmail.com](mailto:wasif.k1112@gmail.com)  
🌐 GitHub: [github.com/wasifkhan](https://github.com/wasifkhan)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


