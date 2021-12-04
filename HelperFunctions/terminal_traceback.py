import pretty_errors


pretty_errors.configure(
    #infix = '\n' + '*'*pretty_errors.exception_writer.get_terminal_width() + '\n',
    display_timestamp         = False,  # uses time.perf_counter()
    inner_exception_separator = True,   # ?  
    line_number_first         = False,  # line number or filename first
    truncate_code           = True,
    # Show lines from previous functions
    trace_lines_before      = 2,
    trace_lines_after       = 2,
    display_trace_locals    = True,
    # Show lines above and bellow the line with the error
    lines_before            = 4,
    lines_after             = 2,
    display_locals          = True,
    # Format of the lines which will be displayed. 
    line_color              = '|' +  pretty_errors.default_config.line_color + pretty_errors.BRIGHT_RED + '-> ' + pretty_errors.default_config.line_color,
    code_color              = '|   ' + pretty_errors.default_config.line_color,
    local_name_color        = '| -> ' + pretty_errors.GREY,
    local_value_color       = '\n' + pretty_errors.BRIGHT_WHITE,
    # Return a link of the location of the error
    display_link            = True,
    # Display name in a specific manner...
    filename_display        = pretty_errors.FILENAME_COMPACT,
    separator_character     = '',
    header_color            = pretty_errors.BRIGHT_RED,
    prefix                  = pretty_errors.BRIGHT_RED + '\n\n' + '*'*pretty_errors.exception_writer.get_terminal_width() + '\n' + ' - Traceback Error\n' + '*'*pretty_errors.exception_writer.get_terminal_width(),
    infix                   = pretty_errors.BRIGHT_CYAN + '-'*pretty_errors.exception_writer.get_terminal_width(),
    postfix                 = '\n' + pretty_errors.BRIGHT_RED + '*'*pretty_errors.exception_writer.get_terminal_width() + '\n\n'
)