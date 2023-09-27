# model settings
model = dict(
    type='AnchorDiffAE',
    encoder=dict(
        type='PartEncoderForTransformerDecoder',
        encoder=dict(
            type='PointNetV2',
            zdim=256,
            point_dim=3,
        ),
        part_aligner=dict(
            type="PartAlignerTransformer",
            in_channels = 256,
            out_channels=6,
            n_class=4,
            d_head=32,
            depth=5,
            n_heads=8,
            dropout=0.,
            use_checkpoint=False,
            use_linear=True,
            class_cond=True,
            single_attn=True,
            add_class_cond=True,
            cimle=True,
            noise_scale=120,
            cond_noise_type=0,
        ),
        n_class=4,
        fit_loss_weight=1.0,
        include_z=False,
        include_part_code=True,
        include_params=True,
        use_gt_params=False,
        fit_loss_type=4
    ),
    diffusion=dict(
        type='AnchoredDiffusion',
        net = dict(
            type='TransformerNet',
            in_channels=3,
            out_channels=3,
            n_heads=8,
            d_head=16,
            depth=5,
            dropout=0.2,
            context_dim=256 + 6,
            n_class=4,
            class_cond=True,
            use_linear=True,
            cat_params_to_x=True,
            use_checkpoint=False,
            single_attn=True,
            cat_class_to_x=True,
        ),
        beta_1=1e-4,
        beta_T=.05,
        k=1.0,
        res=False,
        mode='linear',
        use_beta=False,
        rescale_timesteps=False,
        model_mean_type="epsilon",
        learn_variance=True,
        loss_type='mse',
        include_anchors=False,
        
        classifier_weight=1.,
        guidance=False,
        ddim_sampling=False,
        ddim_nsteps=25,
        ddim_discretize='quad',
        ddim_eta=1.
    ),
    sampler = dict(type='Uniform'),
    num_anchors=4,
    num_timesteps=200,
    npoints = 8192,
    
    cimle=True,
    cimle_sample_num=10,
    ret_traj = False,
    ret_interval = 10,
    forward_sample=False,
    drift_anchors=False,
    interpolate=False,
    combine=False,
    save_weights=False,
    save_dir="/mnt/disk3/wang/diffusion/anchorDIff/work_dirs/pn_aware_attn_both_feat_guidance_200T_no_augment/checkpoints"
)

ids=[3, 2, 14, -1]
data_dir="/orion/u/w4756677/diffusion/spaghetti/assets/checkpoints/spaghetti_chairs_large/None_Chair_10240.pkl"
npoints=8192
scale_mode="shape_unit"
part_scale_mode="shape_canonical"
clip=True
n_class=4

logger = dict(
    type="RunLogger")

# when we the trained model from cshuan, image is rgb
resume_path="work_dirs/anchordiff_exp642/checkpoints/ckpt_1000.pth"