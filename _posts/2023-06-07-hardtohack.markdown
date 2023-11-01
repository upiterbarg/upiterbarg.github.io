---
layout: post
title:  NetHack is Hard to Hack
date:   2023-05-30 00:00:00 +00:00
image: /nh.gif
categories: research
author: "Ulyana Piterbarg, Lerrel Pinto, Rob Fergus"
authors: "<b>Ulyana Piterbarg</b>, Lerrel Pinto, Rob Fergus"
venue: "NeurIPS"
code: https://github.com/upiterbarg/hihack
projectpage: https://upiterbarg.github.io/hihack-demo
arxiv: https://arxiv.org/abs/2305.19240
---
Neural policy learning methods struggle in long-horizon tasks, especially in open-ended environments with multi-modal observations, such as the popular dungeon-crawler game, NetHack. Intriguingly, the NeurIPS 2021 NetHack Challenge revealed that symbolic agents outperformed neural approaches by over four times in median game score. In this paper, we delve into the reasons behind this performance gap and present an extensive study on neural policy learning for NetHack. To conduct this study, we analyze the winning symbolic agent, extending its codebase to track internal strategy selection in order to generate one of the largest available demonstration datasets. Utilizing this dataset, we examine (i) the advantages of an action hierarchy; (ii) enhancements in neural architecture; and (iii) the integration of reinforcement learning with imitation learning. Our investigations produce a <b>state-of-the-art neural agent that surpasses previous fully neural policies by 127% in offline settings and 25% in online settings</b> on median game score. However, we also demonstrate that <b>mere scaling is insufficient to bridge the performance gap with the best symbolic models or even the top human players</b>.