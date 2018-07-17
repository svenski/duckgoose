from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *

def modelForCam(PATH, sz, arch, bs):
    m = arch(True)
    m = nn.Sequential(*children(m)[:-2], 
                      nn.Conv2d(512, 2, 3, padding=1), 
                      nn.AdaptiveAvgPool2d(1),
                      Flatten(), 
                      nn.LogSoftmax())

    tfms = tfms_from_model(arch, sz, aug_tfms=transforms_side_on, max_zoom=1.1)
    data = ImageClassifierData.from_paths(PATH, tfms=tfms, bs=bs)
    learn = ConvLearner.from_model_data(m, data)

    learn.freeze_to(-4)

    return learn


class SaveFeatures():
    features=None
    def __init__(self, m): self.hook = m.register_forward_hook(self.hook_fn)
    def hook_fn(self, module, input, output): self.features = output
    def remove(self): self.hook.remove()


def calculateAndChartHeatZoneFor(input_image, val_tfms, learn):
    m = learn.model
    data = learn.data
    classes = learn.data.classes

    im = val_tfms(np.array(open_image(input_image)))
    actual = inferActualFromPath(input_image, classes)

    preds = learn.predict_array(im[None])
    probs = np.exp(preds)

    d_im = data.val_ds.denorm(im)[0]
    x,y = im[None], probs[0][0]

    conv_features = SaveFeatures(m[-4])
    py = m(Variable(T(x)))
    conv_features.remove()
    py = np.exp(to_np(py)[0])

    feat = np.maximum(0,to_np(conv_features.features[0]))

    non_zeroes_feat = to_np(conv_features.features[0])

    py_orig = py

    dd, gg = heatmapsFor(feat, d_im.shape)

    p_class1= py_orig[0]

    plotCAMHeatmaps(d_im, dd, gg, actual, p_class1, classes)


def inferActualFromPath(im_path, classes):
    os.path.split(im_path)
    actual = "Unknown"

    try:
        pp = os.path.normpath(im_path).split(os.sep)[-2]
    
        if pp in classes:
            actual = pp
    except IndexError:
        print(f'No match for {im_path}')

    return actual


def normalise_img(f2, all_min, all_max):
    return (f2-all_min)/all_max


def resize_img(img, shape):
    return scipy.misc.imresize(img, shape)


def heatmapsFor(feat, shape):
    class1_py = np.array([1, 0])
    class2_py = np.array([0, 1])

    class1_f2=np.dot(np.rollaxis(feat,0,3), class1_py)
    class2_f2=np.dot(np.rollaxis(feat,0,3), class2_py)
    
    all_max = np.concatenate([class1_f2, class2_f2]).max()
    all_min = np.concatenate([class1_f2, class2_f2]).min()
    
    class1_f2 = normalise_img(class1_f2, all_min, all_max)
    class2_f2 = normalise_img(class2_f2, all_min, all_max)
    
    return resize_img(class1_f2, shape), resize_img(class2_f2,shape)


def plotCAMHeatmaps(d_im, dd, gg, actual, p_class1, classes):
    c1 = classes[0]
    c2 = classes[1]

    alpha = 0.7
    fig = plt.figure(figsize=(15,8))
    left_ax = fig.add_subplot(1,3,1)
    left_ax.imshow(d_im)
    left_ax.imshow(dd, alpha=alpha, cmap='hot');
    plt.title(f'{c1} heat zone')
    plt.axis('off')

    middle_ax = fig.add_subplot(1,3,2)
    middle_ax.imshow(d_im)
    plt.title(f'Actual: {actual}. \nPrediction: P({c1})={p_class1:0.2f}')
    plt.axis('off')

    right_ax = fig.add_subplot(1,3,3)
    right_ax.imshow(d_im)
    right_ax.imshow(gg, alpha=alpha, cmap='hot');
    plt.title(f'{c2} heat zone')
    plt.axis('off')

