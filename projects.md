---
layout: default
is_contact: true
---

### [A Bayesian Approach to Modeling Infection-Based Social Distancing in the SARS-CoV-2 Pandemic](docs/socialdistmodel_paper.pdf)
#### 15.077/IDS.147[J]: Statistical Learning and Data Mining, Term Project
> **Abstract**: *In this paper, we use a Bayesian approach to model and analyze the effects of various governments' infection-based social distancing policies during the SARS-CoV-2 pandemic by fitting the [feedback SIR (fSIR) model](https://arxiv.org/pdf/2004.13216.pdf) of disease transmission with linear distancing to observed disease transmission statistics via the PyMC3 probabilistic programming framework. First, we present the assumptions and characteristics of the SIR and fSIR models in more detail. Then, we discuss our experimental methodology for using Bayesian inference to fit the fSIR model with linear distancing to SARS-CoV-2 pandemic data. We also analyze the fit of the model across four different countries with SARS-CoV-2 pandemics (China, France, the United States, and Japan), as well as our resultant, inferred posterior
distributions for model parameters. Lastly, we provide a comparative analysis of various governments' policy responses during the early phases of pandemics and the corresponding, estimated SARS-CoV-2 transmission rates over time derived from the fitted fSIR models.*

This project was completed in early May 2020 and discusses a simple extension of the classical SIR compartmental model of disease transmission that parameterizes infection-based social distancing policy (namely the feedback SIR (fSIR) model imagined by [Dr. Elisa Franco](https://samueli.ucla.edu/people/elisa-franco/)), fitting the model via probabilistic programming against true statistics of infection from four countries with diverse responses to the pandemic. Work was conducted for [Roy E. Welsch](https://mitsloan.mit.edu/faculty/directory/roy-e-welsch)'s graduate class. **Code can be found [here](https://github.com/upiterbarg/epimodelCOVID-19).**

---

### [Exploring strategy learning in the “Tools Environment”](docs/tools_paper.pdf)
#### [6.804: Computational Cognitive Science](https://cbmm.mit.edu/education/courses/computational-cognitive-science), Term Project

> **Abstract**: *Humans are incredibly adept at learning rich contextual information about objects from only a few encounters. With respect to tool use, we are able to quickly master novel problem solving strategies, flexibly identifying how both familiar and unfamiliar objects can be employed to solve challenges confronting us. Here, we run a pilot set of experiments evaluating the [Tools Environment](https://k-r-allen.github.io/tool-games/) as a candidate for computational study of the cognitive processes supporting strategy learning. Participants were asked to solve puzzles requiring the selection and placement of an object in an initially stable 2-D physical scene in order to accomplish goals such as getting an object past a set of obstacles or launching an object into a container. We find that, for three of the four tasks examined here, players' performance in the game improves in a structured manner, corresponding to measurable mastery of increasingly "successful" strategies as more trials are completed.*

I worked under the guidance of Kevin A. Smith and Kelsey R. Allen in the [MIT Computational Cognitive Science Group](http://cocosci.mit.edu/) to conduct the work for this project, using a Bayesian mixture model to analyze collected strategy learning  data.

---

### [Investigating the Efficacy of Option-Conditional Value Prediction in Reinforcement Learning](docs/epfl_srp_poster.pdf)
#### [EPFL School of Life Science Summer Research Program](https://www.epfl.ch/schools/sv/education/summer-research-program/), Poster
Supervised by Johanni Brea and [Wulfram Gerstner](https://lcnwww.epfl.ch/gerstner/), I investigated the efficacy of option-conditional value prediction in reinforcement learning (RL) by adapting the [Value Prediction Network](https://papers.nips.cc/paper/7192-value-prediction-network.pdf)   for tabular environments as well as by implementing the algorithm as in Oh et al.'s original paper, using a combination of temporal-difference search (TD search) and n-step Q-learning for training. The poster linked here was presented to EPFL School of Life Sciences faculty in a summer research colloqium. 