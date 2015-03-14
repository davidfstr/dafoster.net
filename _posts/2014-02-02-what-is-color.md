---
layout: post
title: "What is Color?"
tags: [Offtopic, Personal]

---

Color is a perceived property of light that enters the eye.

Understanding color requires understanding of light, the inputs used by people to detect light (i.e. tristimulous cone responses), and the mental process used to synthesize these inputs into a perceived color.

### Light

Light can be described as a signal: an amplitude that varies over time.

This signal (in the time domain) can be transformed to another signal in the frequency domain which makes it easy to see what individual *frequencies* of light contribute to the overall light signal.

![](/assets/2014/what-is-color/Fourier_transform_time_and_frequency_domains_\(small\).gif)

[Light produced by lasers] is very *coherent*: it only emits light in a narrow frequency band. By contrast the [light produced by the sun] is *full spectrum*, including light in a wide band of frequencies. Having a full spectrum or [high CRI](https://en.wikipedia.org/wiki/Color_rendering_index) light source is desirable for distinguishing colors.

[Light produced by incandescent bulbs] is continuous but heavily-weighted toward the higher (red) frequencies.

[Light produced by florescent bulbs]&nbsp;(CFLs) varies considerably depending on the type of phosphurs used in the bulb.[^ge-spectra] However all CFLs produce *discrete* spectra, combining only a few tiny frequency bands. Discrete spectra (and thus CFLs) are not good for color discrimination.

[Light produced by lasers]: https://en.wikipedia.org/wiki/File:Helium_neon_laser_spectrum.svg
[light produced by the sun]: https://en.wikipedia.org/wiki/File:Solar_Spectrum.png

[Light produced by incandescent bulbs]: http://www.gelighting.com/na/business_lighting/spectral_power_distribution_curves/pop_curves.htm?1
[Light produced by florescent bulbs]: https://en.wikipedia.org/w/index.php?title=Fluorescent_lamp&oldid=593363932#Phosphor_composition
[^ge-spectra]: General Electric provides data about the display spectra for several of its bulbs: <http://www.gelighting.com/na/business_lighting/spectral_power_distribution_curves/>

### Tristimulous Values

A color C as perceived by person P can be described by a tristimulus value (S,M,L) corresponding to the level of excitation of the S-cones, M-cones, and L-cones in the eye of person P.

Cone tristimulus values are ultimately what the brain perceives as color. This is rather interesting because it means that **color is *not* an absolute property of light**. In fact you can have *different* light signals that generate the *same* tristimulous values (i.e. perceived color) in the same person.

### Cone Frequency Responses

Each type of cone is sensitive to different frequencies of light.

Among people who see color normally ("color-normatives"), each type of cone has approximately the same frequency response across individuals:

![](/assets/2014/what-is-color/slide-sml-cones.png)

To obtain the tristimulus value (S,M,L) for a particular light signal, the light signal in the frequency domain must be multiplied by each cone's frequency response graph (or absorbtance graph), and then integrated over the full domain.

### Colorblindness

A person who is colorblind has cone types whose frequency response graphs differ from color-normatives.

Research suggests that the most common type of alteration to the typical frequency response graphs is that the M-cone and L-cone graphs are shifted closer together, making it more difficult to distinguish frequencies close to 550nm (i.e. red and green).

## EnChroma glasses

EnChroma glasses make it easier for colorblind persons (and even color-normative persons) to distinguish colors in the presence of bright full-spectrum light (such as sunlight). These glasses work by reflecting a narrow frequency band between the M-cones and L-cones.[^enchroma-operation]

I speculate that this selective reflection strategy improves color differentiation ability by causing higher contrast between the M-cone and L-cone tristimulus values when *wide-spectrum* reds and greens are viewed through such lenses.

It has been observed that EnChroma glasses do not improve performance on the Ishihara color vision test. This makes sense to me because I expect that these tests use *narrow-spectrum* reds and greens, likely even residing in the frequency band that EnChroma glasses reflect.

In summary I expect EnChroma glasses to be useful in improving color discrimination for full-spectrum light sources such as sunlight, incandescent bulbs, and special full-spectrum "daylight" bulbs. However I do not expect any improvements in color discrimination for narrow-spectrum light sources such as flourescent bulbs, computer monitors, and backlit phone/tablet screens.

[^enchroma-operation]: The discovery underlying EnChroma glasses is documented in this news report: <http://abclocal.go.com/kgo/story?section=news/health&id=8964511>

## Could I make an "EnChroma computer monitor"?

> **Objective:** Find a way to simulate the effect of Enchroma glasses when applied to a computer monitor.

I have seen a programs that filter colors on the screen to attain different effects:

* [f.lux](http://justgetflux.com/): Simulates daylight and dusk-light by altering ambient color temperature.
* [Color Oracle](http://www.colororacle.org/): Simulates colorblind vision for color-normative individuals.[^co-research] Very accurate.

Could I make a filtering program like this that would alter onscreen colors in such a way that a colorblind individual could distinguish them more easily? This would be very useful to me since I am colorblind myself and would like to be able to distinguish colors more easily.

The principal difficulty I foresee is that my computer monitor is probably a narrow-spectrum light source. Indeed the manual for the DELL U2711 (my monitor) does not have any information about its spectral output. So I would need to measure it with a spectrometer or similar instrument. 

Unfortunately Amazon mainly has simple spectrometers that give spectral lines only, not their intensities or the full spectral graph. A spectrometer that can measure the full spectral power distribution currently costs a fair bit more. A few I've noticed:

* [AIBC AI-MK350 Handheld Spectrometer] ($2,000)
* [SpectroCAL Classic Spectroradiometer] (£6,000 ≈ $10,000)


[AIBC AI-MK350 Handheld Spectrometer]: https://www.amazon.com/AIBC-LED-AI-MK350-Handheld-Spectrometer/dp/B0050DAD72/ref=as_sl_pc_ss_til?tag=dafo07-20&linkCode=w01&linkId=&creativeASIN=B0050DAD72

[SpectroCAL Classic Spectroradiometer]: http://www.crsltd.com/tools-for-vision-science/light-measurement-display-calibation/spectrocal-classic-spectroradiometer/


### Additional References

* [Apple > Color Management Overview](https://developer.apple.com/library/mac/documentation/GraphicsImaging/Conceptual/csintro/csintro_intro/csintro_intro.html#//apple_ref/doc/uid/TP30001148)
* [Apple > Color Programming Topics > Color Spaces](https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/DrawColor/Concepts/AboutColorSpaces.html#//apple_ref/doc/uid/20000758-BBCHACHA)



[^co-research]: Color Oracle uses research from: [Digital video colourmaps for checking the legibility of displays by dichromats](http://vision.psychol.cam.ac.uk/jdmollon/papers/colourmaps.pdf)
