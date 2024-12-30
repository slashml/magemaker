
<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">Magemaker v0.1, by SlashML</h3>

  <p align="center">
    Deploy open source AI models to AWS in minutes.
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
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

<!-- ABOUT THE PROJECT -->
## About Magemaker
Magemaker is a Python tool that simplifies the process of deploying an open source AI model to your own cloud. Instead of spending hours digging through documentation to figure out how to get AWS working, Magemaker lets you deploy open source AI models directly from the command line.

Choose a model from Hugging Face or SageMaker, and Magemaker will spin up a SageMaker instance with a ready-to-query endpoint in minutes.

<!-- GETTING STARTED -->
<br>

## Getting Started

Magemaker works with AWS. Azure and GCP support are coming soon!

To get a local copy up and running follow these simple steps.

### Prerequisites

* Python
* An AWS account
* Quota for AWS SageMaker instances (by default, you get 2 instances of ml.m5.xlarge for free)
* Certain Hugging Face models (e.g. Llama2) require an access token ([hf docs](https://huggingface.co/docs/hub/en/models-gated#access-gated-models-as-a-user))

### Configuration

**Step 1: Set up AWS and SageMaker**

To get started, you’ll need an AWS account which you can create at https://aws.amazon.com/. Then you’ll need to create access keys for SageMaker.

We wrote up the steps in [Google Doc](https://docs.google.com/document/d/1NvA6uZmppsYzaOdkcgNTRl7Nb4LbpP9Koc4H_t5xNSg/edit?tab=t.0#heading=h.farbxuv3zrzm) as well. 



### Installing the package

**Step 1**

```sh
pip install magemaker
```

**Step 2: Running magemaker**

Run it by simply doing the following:

```sh
magemaker
```

If this is your first time running this command. It will configure the AWS client so you’re ready to start deploying models. You’ll be prompted to enter your Access Key and Secret here. You can also specify your AWS region. The default is us-east-1. You only need to change this if your SageMaker instance quota is in a different region.

Once configured, it will create a `.env` file and save the credentials there. You can also add your Hugging Face Hub Token to this file if you have one. 

```sh
HUGGING_FACE_HUB_KEY="KeyValueHere"
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE -->
<br>

## Using Magemaker

### Deploying models from dropdown

When you run `magemaker` comamnd it will give you an interactive menu to deploy models. You can choose from a dropdown of models to deploy.

#### Deploying Hugging Face models
If you're deploying with Hugging Face, copy/paste the full model name from Hugging Face. For example, `google-bert/bert-base-uncased`. Note that you’ll need larger, more expensive instance types in order to run bigger models. It takes anywhere from 2 minutes (for smaller models) to 10+ minutes (for large models) to spin up the instance with your model. 

#### Deploying Sagemaker models
If you are deploying a Sagemaker model, select a framework and search from a model. If you a deploying a custom model, provide either a valid S3 path or a local path (and the tool will automatically upload it for you). Once deployed, we will generate a YAML file with the deployment and model in the `CONFIG_DIR=.magemaker_config` folder. You can modify the path to this folder by setting the `CONFIG_DIR` environment variable. 

#### Deploy using a yaml file
We recommend deploying through a yaml file for reproducability and IAC. From the cli, you can deploy a model without going through all the menus. You can even integrate us with your Github Actions to deploy on PR merge. Deploy via YAML files simply by passing the `--deploy` option with local path like so:

```
magemaker --deploy .magemaker_config/bert-base-uncased.yaml
```

Following is a sample yaml file for deploying a model the same google bert model mentioned above:

```yaml
deployment: !Deployment
  destination: aws
  # Endpoint name matches model_id for querying atm.
  endpoint_name: test-bert-uncased
  instance_count: 1
  instance_type: ml.m5.xlarge

models:
- !Model
  id: google-bert/bert-base-uncased
  source: huggingface
```

Following is a yaml file for deploying a llama model from HF:
```yaml
deployment: !Deployment
  destination: aws
  endpoint_name: test-llama2-7b
  instance_count: 1
  instance_type: ml.g5.12xlarge
  num_gpus: 4
  # quantization: bitsandbytes

models:
- !Model
  id: meta-llama/Meta-Llama-3-8B-Instruct
  source: huggingface
  predict:
    temperature: 0.9
    top_p: 0.9
    top_k: 20
    max_new_tokens: 250
```

#### Fine-tuning a model using a yaml file

You can also fine-tune a model using a yaml file, by using the `train` option in the command and passing path to the yaml file

`
magemaker --train .magemaker_config/train-bert.yaml
`

Here is an example yaml file for fine-tuning a hugging-face model:

```yaml
training: !Training
  destination: aws
  instance_type: ml.p3.2xlarge
  instance_count: 1
  training_input_path: s3://jumpstart-cache-prod-us-east-1/training-datasets/tc/data.csv
  hyperparameters: !Hyperparameters
    epochs: 1
    per_device_train_batch_size: 32
    learning_rate: 0.01

models:
- !Model
  id: meta-textgeneration-llama-3-8b-instruct
  source: huggingface
```


<br>
<br>

If you’re using the `ml.m5.xlarge` instance type, here are some small Hugging Face models that work great:
<br>
<br>

**Model: [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased)**

- **Type:** Fill Mask: tries to complete your sentence like Madlibs
- **Query format:** text string with `[MASK]` somewhere in it that you wish for the transformer to fill
- 
<br>
<br>

**Model: [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)**

- **Type:** Feature extraction: turns text into a 384d vector embedding for semantic search / clustering
- **Query format:** "*type out a sentence like this one.*"

<br>
<br>


### Deactivating models

Any model endpoints you spin up will run continuously unless you deactivate them! Make sure to delete endpoints you’re no longer using so you don’t keep getting charged for your SageMaker instance.


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
<br>

## What we're working on next
- [ ]  More robust error handling for various edge cases
- [ ]  Verbose logging
- [ ]  Enabling / disabling autoscaling
- [ ]  Deployment to Azure and GCP

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ISSUES -->
<br>

## Known issues
- [ ]  Querying within Magemaker currently only works with text-based model - doesn’t work with multimodal, image generation, etc.
- [ ]  Deleting a model is not instant, it may show up briefly after it was queued for deletion
- [ ]  Deploying the same model within the same minute will break

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->
<br>

## License

Distributed under the Apache 2.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
<br>

## Contact

You can reach us, faizan & jneid, at [support@slashml.com](mailto:support@slashml.com). 

We’d love to hear from you! We’re excited to learn how we can make this more valuable for the community and welcome any and all feedback and suggestions.
