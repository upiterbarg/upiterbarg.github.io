---
layout: post
title:  NetHack is Hard to Hack
date:   2023-05-30 00:00:00 +00:00
image: /nh.gif
categories: research
author: "Ulyana Piterbarg, Lerrel Pinto, Rob Fergus"
authors: "<b>Ulyana Piterbarg</b>, Lerrel Pinto, Rob Fergus"
venue: "37th Conference on Neural Information Processing Systems (NeurIPS)"
code: https://github.com/upiterbarg/hihack
projectpage: https://upiterbarg.github.io/hihack-demo
arxiv: https://arxiv.org/abs/2305.19240
---
Neural policy learning methods struggle in long-horizon tasks, especially in open-ended environments with multi-modal observations, such as the popular dungeon-crawler game, NetHack. In the NeurIPS 2021 NetHack Challenge, symbolic agents outperformed neural approaches by over four times in median game score. In this paper, we delve into the reasons behind this performance gap and present an extensive study on neural policy learning for NetHack. Our investigations produce a state-of-the-art neural agent. However, we also demonstrate that **scaling up supervised learning is insufficient to bridge the performance gap with the best symbolic models or even the top human players**.