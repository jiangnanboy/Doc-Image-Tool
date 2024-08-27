<p align="left">
    <span>
        <b>中文</b>
    </span>
    <span> • </span>
    <a href="README_en.md">
        English
    </a>
</p>

<h1 align="center">Doc-Image-Tool 文档图像处理工具</h1>
<br>
<div align="center">
  <strong>免费，开源，用于文档图像的处理软件</strong><br>
</div><br>

- **免费**：本项目所有代码开源，完全免费。
- **方便**：解压即用，离线运行，无需网络。
- **功能**：漂白 / 文字方向矫正 / 清晰增强 / 笔记去噪美化 / 去阴影 / 扭曲矫正 / 切边增强

<p align="center"><img src="imgs/main.png"></p>

## 目录

- [漂白](#漂白)
- [文字方向矫正](#文字方向矫正)
- [清晰增强](#清晰增强)
- [笔记去噪美化](#笔记去噪美化)
- [去阴影](#去阴影)
- [扭曲矫正](#扭曲矫正)
- [切边增强](#切边增强)

## 开始使用

目前使用方法，你只需下载本项目源码，找到main.py，运行即可。

weights下的模型包括扭曲矫正、清晰增强以及切边增强三个，百度网盘下载：

链接: https://pan.baidu.com/s/1Ty_JSYcauRX0MiIRuhxx_w 提取码: 92vb

遇到任何问题，请提 [Issue](https://github.com/jiangnanboy/Doc-Image-Tool/issues) ，我会尽可能帮助你。

### 漂白
对文档图像进行漂白。

<p align="center"><img src="imgs/漂白_raw.png"></p>

<p align="center"><img src="imgs/漂白_result.png"></p>

### 文字方向矫正
对文档图像进行文字方向矫正。

<p align="center"><img src="imgs/文字方向_raw.png"></p>

<p align="center"><img src="imgs/文字方向_result.png"></p>

### 清晰增强
对文档图像进行清晰增强，可以对任意一张图像增强清晰度，这会增大图像尺寸。

### 笔记去噪美化
对手写体笔记图像进行去噪美化。

<p align="center"><img src="imgs/去噪美化_raw.png"></p>

<p align="center"><img src="imgs/去噪美化_result.png"></p>

### 去阴影
对文档图像去除阴影。

<p align="center"><img src="imgs/去阴影_raw.png"></p>

<p align="center"><img src="imgs/去阴影_result.png"></p>

### 扭曲矫正
对文档图像进行扭曲矫正。

<p align="center"><img src="imgs/扭曲矫正_raw.png"></p>

<p align="center"><img src="imgs/扭曲矫正_result.png"></p>

### 切边增强
对文档图像进行切边，提取并突出主体部分。

<p align="center"><img src="imgs/切边_raw.png"></p>

<p align="center"><img src="imgs/切边_result.png"></p>

---

### 工程的核心算法源码：

```
function_method
├─ DocBleach #漂白
├─ TextOrientationCorrection #文字方向矫正
├─ DocSharpening #清晰增强
├─ HandwritingDenoisingBeautifying #笔记去噪美化
├─ DocShadowRemoval #去阴影
├─ document_image_dewarping #扭曲矫正
└─ DocTrimmingEnhancement #切边增强

```
---

## 赞助

Doc-Image-Tool 项目主要由作者 [jiangnanboy](https://github.com/jiangnanboy) 用业余时间在开发和维护。如果您喜欢这款软件，欢迎赞助，这也是作者的动力之一。

- 国内用户可通过 [爱发电](https://afdian.com/a/jiangnanboy) 赞助作者。

## 开发计划

<details>
<summary>已完成的工作</summary>

- 漂白
- 文字方向矫正
- 清晰增强
- 笔记去噪美化
- 去阴影
- 扭曲矫正
- 切边增强

</details>

##### 正在进行的工作，或者如果你有什么好的功能建议，也请提出【建议】，我会尽量实现功能需求。

- [ ] 去黑点。
- [ ] 去水印。
- [ ] 去印章。
- [ ] 手写体擦除。

##### 持续及远期计划

<details>
<summary>展开</summary>

以下是未来计划。

- [ ] 重构界面。
- [ ] 加入更多文档图像处理功能。
- [ ] 加入OCR功能。
- [ ] 加入表格识别功能。
- [ ] 加入文档图像多模态问答功能。

</details>

## Contact
如有问题，联系我：

1、github：https://github.com/jiangnanboy

2、QQ:2229029156
