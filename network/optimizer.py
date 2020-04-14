import dlib
import math
from configs import g_conf



def adjust_learning_rate(optimizer, num_iters):
    """
    Adjusts the learning rate every epoch based on the selected schedule
    """
    cur_iters = num_iters
    minlr = 0.0000001
    scheduler = "normal"
    learning_rate = g_conf.LEARNING_RATE
    decayinterval = g_conf.LEARNING_RATE_DECAY_INTERVAL
    decaylevel = g_conf.LEARNING_RATE_DECAY_LEVEL
    if scheduler == "normal":
        while cur_iters >= decayinterval:
            learning_rate = learning_rate * decaylevel
            cur_iters = cur_iters - decayinterval
        learning_rate = max(learning_rate, minlr)

    for param_group in optimizer.param_groups:
        print("New Learning rate is ", learning_rate)
        param_group['lr'] = learning_rate


def adjust_learning_rate_auto(optimizer, loss_window):
    """
    Adjusts the learning rate every epoch based on the selected schedule
    """
    minlr = 0.0000001
    learning_rate = g_conf.LEARNING_RATE
    thresh = g_conf.LEARNING_RATE_THRESHOLD
    decaylevel = g_conf.LEARNING_RATE_DECAY_LEVEL
    n = 1000
    start_point = 0
    while n < len(loss_window):
        steps_no_decrease = dlib.count_steps_without_decrease(loss_window[start_point:n])
        steps_no_decrease_robust = dlib.count_steps_without_decrease_robust(loss_window[start_point:n])
        if steps_no_decrease > thresh and steps_no_decrease_robust > thresh:
            start_point = n
            learning_rate = learning_rate * decaylevel

        n += 1000

    learning_rate = max(learning_rate, minlr)

    for param_group in optimizer.param_groups:
        param_group['lr'] = learning_rate


def adjust_learning_rate_cosine_annealing(optimizer, loss_window, iteration):
    """
    Adjusts the learning rate based on cyclic cosine annealing https://arxiv.org/pdf/1704.00109.pdf
    Adam converges within 100k iterations so lets assume 5 cycles of 20k iterations each
    """
    initial_lr = g_conf.LEARNING_RATE
    learning_rate= initial_lr*(math.cos(math.pi*((iteration-1)%20000)/20000)+1)

    for param_group in optimizer.param_groups:
        # print("New Learning rate is ", learning_rate)
        param_group['lr'] = learning_rate