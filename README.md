<a name="readme-top"></a>

<br />
<div align="center">
  <h3 align="center">Magemaker by SlashML</h3>

  <p align="center">
    Deploy open source AI models to AWS, GCP, and Azure in minutes.
    <br />
    <a href="https://magemaker.slashml.com"><strong>📚 Documentation »</strong></a>
    <br />
    <br />
    <a href="https://discord.gg/SBQsD63d">Join our Discord</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-model-manager">About Magemaker</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#using-model-manager">Using Magemaker</a></li>
    <li><a href="#what-were-working-on-next">What we're working on next</a></li>
    <li><a href="#known-issues">Known issues</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About Magemaker
Magemaker is a Python tool that simplifies the process of deploying an open source AI model to your own cloud. Instead of spending hours digging through documentation, Magemaker lets you deploy Hugging Face models directly to AWS SageMaker, Google Cloud Vertex AI, or Azure Machine Learning.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python 3.11+ (except 3.12)
* Cloud provider account(s):
  * AWS for SageMaker
  * GCP for Vertex AI
  * Azure for Azure ML
* Cloud CLI tools:
  * AWS CLI (optional)s
  * Google Cloud SDK for GCP
  * Azure CLI for Azure
* Hugging Face account (for access to models)

### Installing the package

```sh
pip install magemaker
```

Run it by simply doing the following:

```sh
magemaker
```

The first time you run this command, it will ask you for a cloud provider flag. You can specify it using `magemaker --cloud gcp`. The possible options for cloud provider flags are `gcp|aws|azure|all`, where `all` will configure all providers. If this is your first time running it, it will take some time to configure it. You'll be guided through setting up your chosen cloud provider(s).

## Using Magemaker

### Deploying models from dropdown

When you run `magemaker` command it will give you an interactive menu to deploy models. You can choose from a dropdown of models to deploy.

### Deploy using a yaml file

We recommend deploying through a yaml file for reproducibility and IAC. Deploy via YAML files by passing the `--deploy` option:

```sh
magemaker --deploy .magemaker_config/model-config.yaml
```

Example YAML files for deploying facebook/opt-125m:

AWS (SageMaker):
```yaml
deployment: !Deployment
  destination: aws
  endpoint_name: facebook--opt-125m
  instance_count: 1
  instance_type: ml.m5.xlarge

models:
- !Model
  id: facebook/opt-125m
  source: huggingface
  task: text-generation
```

GCP (Vertex AI):
```yaml
deployment: !Deployment
  destination: gcp
  endpoint_name: test-endpoint-12
  accelerator_count: 1
  instance_type: g2-standard-12
  accelerator_type: NVIDIA_L4

models:
- !Model
  id: facebook/opt-125m
  source: huggingface
```

Azure ML:
```yaml
deployment: !Deployment
  destination: azure
  endpoint_name: facebook--opt-125m
  instance_count: 1
  instance_type: Standard_DS3_v2

models:
- !Model
  id: facebook/opt-125m
  source: huggingface
  task: text-generation
```

### Deactivating models

⚠️ Any model endpoints you spin up will run continuously unless you deactivate them! Make sure to delete endpoints you're no longer using to avoid unnecessary charges.

## What we're working on next
- [ ] More robust error handling for various edge cases
- [ ] Verbose logging
- [ ] Enabling / disabling autoscaling
- [ ] Enhanced multi-cloud support features

## Known issues
- [ ] Querying within Magemaker currently only works with text-based models
- [ ] Deleting a model is not instant, it may show up briefly after deletion
- [ ] Deploying the same model within the same minute will break

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

## Contact

You can reach us through:
- Email: [support@slashml.com](mailto:support@slashml.com)
- Discord: [Join our community](https://discord.gg/SBQsD63d)
- Documentation: [magemaker.slashml.com](https://magemaker.slashml.com)

We'd love to hear from you! We're excited to learn how we can make this more valuable for the community and welcome any and all feedback and suggestions.