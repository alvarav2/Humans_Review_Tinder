import argparse
import sys
import numpy as np
import torch
from meta_optimizer import MetaModel, MetaOptimizer, FastMetaOptimizer
from learner import Learner
from torch.autograd import Variable
from torchvision import datasets, transforms
import pipeline as data
from pprint import pprint


parser = argparse.ArgumentParser ()

parser.add_argument("--NumShots", type=int, help="Num of shotst to train on", default=4)
parser.add_argument("--NumClasses", type=int, help="Num of classes to train on", default=5)
parser.add_argument("--BatchSize", type=int, help="Num of batches in one episode", default=5)

parser.add_argument('--batch_size', type=int, default=32, metavar='N',
                    help='batch size (default: 32)')
parser.add_argument('--optimizer_steps', type=int, default=.01, metavar='N',
                    help='number of meta optimizer steps (default: .01)')
parser.add_argument('--truncated_bptt_step', type=int, default=20, metavar='N',
                    help='step at which it truncates bptt (default: 20)')
parser.add_argument('--updates_per_epoch', type=int, default=10, metavar='N',
                    help='updates per epoch (default: 10)')
parser.add_argument('--max_epoch', type=int, default=100, metavar='N',
                    help='number of epoch (default: 100)')
parser.add_argument('--hidden_size', type=int, default=10, metavar='N',
                    help='hidden size of the meta optimizer (default: 10)')
parser.add_argument('--num_layers', type=int, default=3, metavar='N',
                    help='number of LSTM layers (default: 3)')
args = parser.parse_args ()
#
#assert args.optimizer_steps % args.truncated_bptt_step == 0
#
#kwargs = {'num_workers': 1, 'pin_memory': True} if torch.cuda.is_available () else {}
#train_loader = torch.utils.data.DataLoader(
#    datasets.MNIST('../data', train=True, download=True,
#                   transform=transforms.Compose([
#                       transforms.ToTensor(),
#                       transforms.Normalize((0.1307,), (0.3081,))
#                   ])),
#    batch_size=args.batch_size, shuffle=True, **kwargs)
#test_loader = torch.utils.data.DataLoader(
#    datasets.MNIST('../data', train=False, transform=transforms.Compose([
#                       transforms.ToTensor(),
#                       transforms.Normalize((0.1307,), (0.3081,))
#                   ])),
#    batch_size=args.batch_size, shuffle=True, **kwargs)



def main ():
    """Main Routine"""

    #-------------- Pipline Initialization --------------
    pipeline = data.Pipeline (args.NumShots, args.NumClasses)
    #-------------- Pipline Initialization --------------

    #-------------- Loss Function Initialization --------------
    criterion = torch.nn.CrossEntropyLoss ()
    #-------------- Loss Function Initialization --------------

    #-------------- Model Initialization --------------
    # Initialize the shadow learner
    shadow_learner = Learner (args.NumClasses, args.BatchSize, "relu")
    if torch.cuda.is_available ():
        shadow_learner.cuda ()
    # Initialize the meta learner
    meta_learner = FastMetaOptimizer (MetaModel (shadow_learner), args.num_layers, args.hidden_size)
    if torch.cuda.is_available ():
        meta_learner.cuda ()
    optimizer = torch.optim.Adam (meta_learner.parameters (), lr=0.001)
    #-------------- Model Initialization --------------

    #------------- Initialize Loss Metric -------------
    decrease_in_loss = 0.0
    final_loss = 0.0
    #------------- Initialize Loss Metric -------------

#    # Initialize MNIST iterator
#    train_iter = iter (train_loader)
#    dev_iter = iter (test_loader)


    epoch = 1
    # Loop until no episodes left
    episode_count = 1
    while(epoch < args.max_epoch):

        while True:

            print ("-------------")
            print ("Episode: " + str (episode_count))
            print ("-------------")
            episode_count += 1

            #------------- Learner Initailization -------------
            learner = Learner (args.NumClasses, args.BatchSize, "relu")
            if torch.cuda.is_available ():
                learner.cuda ()
            #------------- Learner Initailization -------------

            # Get one batch of mnist for the initial loss
    #            x, y = next (train_iter)
    #            if torch.cuda.is_available ():
    #                x, y = x.cuda (), y.cuda ()
    #            x, y = Variable (x), Variable (y)

            #-------------- Episode Loading --------------
            # Get an episode from the pipeline
            episode = pipeline.next_episode ()
            # Check if no more episode
            if episode == False:
                break

            # Get train set from episode
            train_x, train_y = episode.train_x, episode.train_y
            train_size =  args.NumShots * args.NumClasses
            idx = np.random.permutation (train_size)
            train_x = train_x [idx, :]
            train_y = train_y [idx]
            if torch.cuda.is_available ():
                train_x, train_y = train_x.cuda (), train_y.cuda ()

            train_x, train_y = Variable (train_x), Variable (train_y)
            #-------------- Episode Loading --------------

            #---------- Initalize Learner Loss Metric ----------
    #            learner_pred = learner (x)
    #            initial_loss = torch.nn.functional.nll_loss (learner_pred, y)
            initial_loss = torch.Tensor([1.0])
            #---------- Initalize Learner Loss Metric ----------



            #for k in range (args.optimizer_steps // args.truncated_bptt_step):

            # Keep states for truncated BPTT
    #        meta_learner.reset_lstm (keep_states=k > 0, model=learner, use_cuda=torch.cuda.is_available ())
            meta_learner.reset_lstm (True, model=learner, use_cuda=torch.cuda.is_available ())



            # Loop thru all batches of the episode
            # for j in range (args.truncated_bptt_step):
            num_batches = train_size // args.BatchSize
            for j in range (num_batches):
                # print ("-------------")
                # print ("Batch: " + str (j + 1))
                # print ("-------------")

                #--------------- Learner Update ----------------
                # Get train batch from mnist
    #                    x, y = next (train_iter)
    #                    if torch.cuda.is_available ():
    #                        x, y = x.cuda (), y.cuda ()
    #                    x, y = Variable (x), Variable (y)
                # Get a train batch from eposide
                start = j * args.BatchSize
                end = start + args.BatchSize
                x = train_x [start : end].reshape ((args.BatchSize, 1, 129, 1822))
                y = train_y [start : end]
                # Get learner loss
                learner_pred = learner (x, False)
    #                    loss = torch.nn.functional.nll_loss (learner_pred, y)
                loss = criterion (learner_pred, y)
                # Get learner gradients
                learner.zero_grad ()
                loss.backward ()
                # Update learner and shadow learner parameters
                shadow_learner = meta_learner.update_learner_params (learner, loss.detach())
                print("loss is  for training", loss.detach().item())
                #--------------- Learner Update ----------------

            #--------------- Meta Learner Update ----------------
            # Get dev batch from mnist
    #                dev_x, dev_y = next (dev_iter)
    #                if torch.cuda.is_available ():
    #                    dev_x, dev_y = dev_x.cuda (), dev_y.cuda ()
    #                dev_x, dev_y = Variable (dev_x), Variable (dev_y)
            # Get dev set from episode
            dev_x, dev_y = episode.dev_x.reshape ((10, 1, 129, 1822)), episode.dev_y
            if torch.cuda.is_available ():
                dev_x, dev_y = dev_x.cuda (), dev_y.cuda ()
            dev_x, dev_y = Variable (dev_x), Variable (dev_y)
            # Get shadow learner loss
            learner_pred = shadow_learner (dev_x, True)
    #                loss = torch.nn.functional.nll_loss (learner_pred, dev_y)
            dev_loss = criterion (learner_pred, dev_y)
            # Get meta learner gradients
            meta_learner.zero_grad ()
            dev_loss.backward ()
            print("Post episode loss is ", dev_loss.detach().item())
            with open("output_new.txt", "a") as f:
                f.write ("Episode ")
                f.write (str (episode_count))
                f.write (str (dev_loss.detach().item()))
            # Clip meta learner gradients
            for param in meta_learner.parameters ():
                param.grad.data.clamp_ (-1, 1)
            # Update meta learner parameters
            optimizer.step ()
            #---------------- Meta Learner Update ----------------

            # Compute relative decrease in the loss function w.r.t initial value

            #decrease_in_loss += loss.item () / initial_loss.item ()
            #final_loss += loss.item ()
            #if(episode_count % 60 == 0):
                #print("Epoch: {}, final loss {}, average final/initial loss ratio: {}".format(epoch, final_loss / args.updates_per_epoch,
                                                                               #decrease_in_loss / args.updates_per_epoch))
                #with open("output.txt", "a") as f:
                    #f.write("number of LSTM layers (default: 3): epoch %d , final loss %f , average final/intial_lost ratio %f\n" %  (epoch, final_loss / args.updates_per_epoch, decrease_in_loss / args.updates_per_epoch))
        epoch += 1
if __name__ == "__main__":
    main()
