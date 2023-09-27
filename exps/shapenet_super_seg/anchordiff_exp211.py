# model settings
import torch
cimle=True
cimle_cache_interval=10
model = dict(
    type='AnchorDiffAE',
    sample_noise_num=128,
    encoder=dict(
        type='PartEncoderCIMLE',
        encoder=dict(
            type='PointNetV2',
            zdim=256,
            point_dim=3,
        ),
        mixer=dict(
            type="PartCodeTransformerV2",
            device='cuda' if torch.cuda.is_available() else 'cpu',
            input_channels=256,
            n_ctx=4,
            output_channels=256,
            width=256,
            layers=5,
            heads=8,
            init_scale=0.25,
            class_cond=True,
            param_cond=True,
            post_mlp=True
        ),
        part_aligner=dict(
            type="PartAlignerCIMLE",
            n_class=4,
            width=256,
            param_dim=3,
            noise_dim=32
        ),
        include_var=True,
        n_class=4,
        include_z=True,
        include_part_code=False,
        include_params=True,
        part_code_dropout_prob=0.0,
        param_dropout_prob=0.0
    ),
    diffusion=dict(
        type='AnchoredDiffusion',
        net = dict(
            type='PointwiseNet',
            in_channels=3,
            out_channels=3,
            res=True,
            context_dim=256 + 6,
        ),
        beta_1=1e-4,
        beta_T=.05,
        k=1.0,
        res=False,
        mode='linear',
        use_beta=True,
        rescale_timesteps=False,
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
    npoints = 2048,
    anchor_loss_weight=1.,
    
    ret_traj = False,
    ret_interval = 10,
    forward_sample=False,
    interpolate=False,
    save_weights=False,
    save_dir="/mnt/disk3/wang/diffusion/anchorDIff/work_dirs/pn_aware_attn_both_feat_guidance_200T_no_augment/checkpoints"
)

dataset = dict(
    train=dict(
        type="ShapeNetSegPart",
        batch_size = 128,
        split='trainval',
        root='/orion/group/shapenetcore_partanno_segmentation_benchmark_v0_normal',
        eval_mode='ae',
        npoints=2048,
        scale_mode='shape_unit',
        num_workers=4,
        class_choice='Chair',
        augment=True,
    ),
    val=dict(
        type="ShapeNetSegPart",
        batch_size=32,
        split='test',
        eval_mode='ae',
        root='/orion/group/shapenetcore_partanno_segmentation_benchmark_v0_normal',
        npoints=2048,
        shuffle=False,
        scale_mode='shape_unit',
        num_workers=0,
        class_choice='Chair',
        save_only=True
    ),
)

optimizer = dict(type='Adam', lr=0.001, weight_decay=0.)

scheduler = dict(
    type='StepLR',
    step_size=2666,
    gamma=0.5,
)

logger = dict(
    type="RunLogger")

# when we the trained model from cshuan, image is rgb
save_num_batch = 1
max_epoch = 8000
eval_interval = 500
checkpoint_interval = 2000
log_interval = 50
max_norm=10
eval_both=True
