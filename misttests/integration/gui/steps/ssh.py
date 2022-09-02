import re

from behave import step

from time import time
from time import sleep

from misttests.integration.gui.steps.buttons import clicketi_click

from misttests.integration.gui.steps.utils import safe_get_element_text, expand_shadow_root

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def is_ssh_connection_up(lines):
    errors = ['disconnected', 'timeout', 'timed out', 'closure', 'broken']
    for line in lines:
        for error in errors:
            if error in line.lower():
                return False
    return True


def update_lines(context, terminal, lines):
    """
    Scans through the terminal lines to find new ones and update any line that
    has changed(for example when a command is given and enter is pressed).
    """
    starting_lines = len(lines)
    line_has_been_updated = False
    context.browser.execute_script("arguments[0].term.selectAll();", terminal)
    all_lines = context.browser.execute_script("return arguments[0].term.getSelection();", terminal).split("\n")
    context.browser.execute_script("arguments[0].term.clearSelection();", terminal)
    i = len(all_lines) - 1
    while i >= 0:
        if all_lines[i] != "":
            break
        i -= 1
    all_lines = all_lines[:i+1]
    safety_counter = max_safety_count = 5
    for i in range(0, len(all_lines)):
        line = all_lines[i].rstrip().lstrip()
        if line:
            if i < starting_lines and lines[i] != line:
                lines[i] = line
                line_has_been_updated = True
            elif i >= starting_lines:
                lines.append(line)
        safety_counter = safety_counter - 1 if not line else max_safety_count
        if safety_counter == 0:
            break
    return starting_lines < len(lines) or line_has_been_updated


def check_ls_output(lines, filename=None):
    """
    Checks the output of the ls command and if a filename is provided whether
    or not the file is included in the output of the ls command
    """
    command_output_end_line = len(lines)
    command_output_start_line = 0
    # find where the ls output starts and ends
    for i in range(len(lines)-1, 0, -1):
        if re.search("total\s\d+", lines[i]) and \
                re.search(":.*(\$|#).*.*ls.*", lines[i-1]) and \
                command_output_start_line < i:
            command_output_start_line = i
            break
        if re.search(":.*(\$|#).*", lines[i]) and command_output_end_line > i:
            command_output_end_line = i - 1
    if command_output_start_line == 0:
        assert False, "Could not find the output of the ls command. Contents" \
                      " of the terminal are: %s" % lines
    if not filename:
        return True
    for i in range(command_output_end_line, command_output_start_line, -1):
        if filename in lines[i]:
            return True
    assert False, "File with name %s is not listed in the output of the ls " \
                  "command. Contents of the terminal are: %s" & lines


@step('I expect terminal to open within {seconds} seconds')
def terminal_is_open(context, seconds):
    terminal = None
    end_time = time() + int(seconds)
    while time() < end_time:
        if (len(context.browser.window_handles) < 2):
            continue
        try:
            context.browser.switch_to.window(context.browser.window_handles[1])
            terminal = context.browser.find_element(By.CSS_SELECTOR, '.xterm-helpers')
            break
        except NoSuchElementException:
            sleep(1)
    assert terminal, "Terminal has not opened after pressing the " \
                     "button. Aborting!"


@step('shell input should be {state} after {seconds} seconds')
def check_shell_input_state(context, state, seconds):
    if state not in ['available', 'unavailable']:
        raise ValueError('Unknown type of state')
    lines = []
    try:
        context.browser.switch_to.window(context.browser.window_handles[1])
    except Exception as exc:
        print("Failed to find new window")
        raise(exc)
    terminal_container = context.browser.find_element(By.CSS_SELECTOR, "#terminal-container")
    max_time = time() + int(seconds)
    while time() < max_time:
        if update_lines(context, terminal_container, lines):
            assert is_ssh_connection_up(lines), "Error while using shell"
            if state == 'available' and re.search(":(.*)(\$|#)\s?$", lines[-1]):
                break
            elif state == 'unavailable' and re.search(":(.*)(\$|#)\s?$", lines[-1]):
                assert False, "Shell input is available although it shouldn't be!"
        if state == 'available':
            assert time() + 1 < max_time, "Shell hasn't connected after" \
                                      " %s seconds. Aborting!" \
                                                 % seconds


@step('I type in the terminal "{command}"')
def type_in_terminal(context, command):
    try:
        context.browser.switch_to.window(context.browser.window_handles[1])
    except Exception as exc:
        print("Failed to find new window")
        raise(exc)
    terminal_container = context.browser.find_element(By.CSS_SELECTOR, "#terminal-container")
    msg = '' + command
    context.browser.execute_script("arguments[0].term.paste('{}');".format(msg), terminal_container)
    context.browser.execute_script("""document.querySelector('textarea').dispatchEvent(
        new KeyboardEvent('keydown', {
            altKey:false, bubbles: true, cancelBubble: false,
            cancelable: true, charCode: 0, code: 'Enter', composed: true,
            ctrlKey: false, currentTarget: null, defaultPrevented: true,
            detail: 0, eventPhase: 0, isComposing: false, isTrusted: true,
            key: 'Enter', keyCode: 13, location: 0, metaKey: false,
            repeat: false, returnValue: false, shiftKey: false,
            type: 'keydown', which: 13
        }))""", terminal_container)


@step('{output} should be included in the output')
def check_output(context, output):
    try:
        context.browser.switch_to.window(context.browser.window_handles[1])
    except Exception as exc:
        print("Failed to find new window")
        raise(exc)
    terminal_container = context.browser.find_element(By.CSS_SELECTOR, "#terminal-container")
    context.browser.execute_script("arguments[0].term.selectAll();", terminal_container)
    shell_text = context.browser.execute_script(
        "return arguments[0].term.getSelection();", terminal_container)
    context.browser.execute_script(
        "arguments[0].term.clearSelection();", terminal_container)
    # This is used in mayday test at the moment of writing
    if "||" in output:
        [output1, output2] = output.split("||")
        if output1.strip() in shell_text:
            return
        if output2.strip() in shell_text:
            return
    elif output in shell_text:
        return
    assert False, "%s is not included in the shell's output." % output


@step('I close the terminal')
def close_terminal(context):
    try:
        context.browser.switch_to.window(context.browser.window_handles[1])
    except Exception as exc:
        print("Failed to find new window")
        raise(exc)
    context.browser.close()
    assert len(context.browser.window_handles) == 1, "There is more than one window opened!!"
    context.browser.switch_to.window(context.browser.window_handles[0])


def check_ssh_connection_with_timeout(context,
                                      connection_timeout=200,
                                      filename=None):
    end_time = time() + 10
    terminal = None
    while time() < end_time:
        try:
            terminal = context.browser.find_element(By.CSS_SELECTOR, '.terminal')
            sleep(1)
            break
        except NoSuchElementException:
            sleep(1)
    assert terminal, "Terminal has not opened 10 seconds after pressing the " \
                     "button. Aborting!"

    connection_max_time = time() + connection_timeout
    lines = []

    # waiting for input to become available
    while time() < connection_max_time:
        if update_lines(terminal, lines):
            assert is_ssh_connection_up(lines), "Error while using shell"
            if re.search(":(.*)(\$|#)\s?$", lines[-1]):
                break
        assert time() + 1 < connection_max_time, "Shell hasn't connected after"\
                                                 " %s seconds. Aborting!"\
                                                 % connection_timeout
        sleep(1)
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    xterm_dialog = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
    contect.browser.execute_script("arguments[0].term.paste('ls -l\n')", xterm_dialog)
    # remove the last line so that it can be updated since the command has
    # been added
    lines = lines[:-1]
    command_end_time = time() + 20
    # waiting for command output to be returned
    while time() < command_end_time:
        # if the command output has finished being printed
        if update_lines(terminal, lines):
            assert is_ssh_connection_up(lines), "Connection is broken"
            # If it looks like the execution of the command has finished
            if re.search(":(.*)(\$|#)\s?$", lines[-1]):
                try:
                    # look if the result has returned
                    check_ls_output(lines, filename)
                    return
                except AssertionError as e:
                    if time() > command_end_time:
                        raise e
        sleep(1)
    assert False, "Command output took too long"

# Following steps are for docker kubevirt libvirt which open the terminal in the page

@step('I expect in-page terminal to open within {seconds} seconds')
def in_page_terminal_is_open(context, seconds):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    end_time = time() + int(seconds)
    terminal = None
    while time() < end_time:
        try:
            terminal = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
            break
        except NoSuchElementException:
            sleep(1)
    assert terminal, "Terminal has not opened after pressing the " \
                     "button. Aborting!"


@step('in-page shell input should be {state} after {seconds} seconds')
def check_in_page_shell_input_state(context, state, seconds):
    if state not in ['available', 'unavailable']:
        raise ValueError('Unknown type of state')
    lines = []
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    xterm_dialog = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
    max_time = time() + int(seconds)
    while time() < max_time:
        if update_lines(context, xterm_dialog, lines):
            assert is_ssh_connection_up(lines), "Error while using shell"
            if state == 'available' and re.search(":(.*)(\$|#)\s?$", lines[-1]):
                break
            elif state == 'unavailable' and re.search(":(.*)(\$|#)\s?$", lines[-1]):
                assert False, "Shell input is available although it shouldn't be!"
        if state == 'available':
            assert time() + 1 < max_time, "Shell hasn't connected after" \
                                      " %s seconds. Aborting!" \
                                                 % seconds


@step('{filename} should be included in the in-page terminal output')
def check_in_page_terminal_output(context, filename):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    xterm_dialog = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
    context.browser.execute_script("arguments[0].term.selectAll();", xterm_dialog)
    shell_text = context.browser.execute_script(
        "return arguments[0].term.getSelection();", xterm_dialog)
    context.browser.execute_script(
        "arguments[0].term.clearSelection();", xterm_dialog)
    if filename in shell_text:
        return
    assert False, "%s is not included in the shell's output." % filename


@step('I type in the in-page terminal "{command}"')
def type_in_in_page_terminal(context, command):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    xterm_dialog = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
    msg = '' + command
    context.browser.execute_script("arguments[0].term.paste('{}');".format(msg), xterm_dialog)
    action = ActionChains(context.browser)
    action.send_keys(Keys.ENTER)
    action.perform()

@step('I close the in-page terminal')
def close_in_page_terminal(context):
    mist_app = context.browser.find_element(By.CSS_SELECTOR, 'mist-app')
    mist_app_shadow = expand_shadow_root(context, mist_app)
    xterm_dialog = mist_app_shadow.find_element(By.CSS_SELECTOR, 'xterm-dialog')
    close_button = expand_shadow_root(context, xterm_dialog).find_element(By.CSS_SELECTOR, 'paper-button')
    clicketi_click(context, close_button)
    WebDriverWait(mist_app_shadow, 4).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'xterm-dialog')))
